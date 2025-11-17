#!/usr/bin/env python3
"""
Phase 2: Google Cloud Storage Upload Script

Uploads ADK knowledge corpus to Google Cloud Storage for use with
Gemini File Search and Agent Builder Pro.

Prerequisites:
- Google Cloud SDK configured
- GCS APIs enabled
- Appropriate IAM permissions

Outputs:
- GCS bucket with all knowledge corpus files
- upload_manifest.json with upload metadata
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from google.cloud import storage
    from google.api_core import exceptions
except ImportError:
    print("ERROR: google-cloud-storage not installed")
    print("Install with: pip install google-cloud-storage")
    sys.exit(1)


class GCSKnowledgeUploader:
    """Uploads ADK knowledge corpus to Google Cloud Storage."""

    def __init__(
        self,
        project_id: str,
        bucket_name: str,
        source_dir: str = "knowledge_corpus",
        location: str = "us-central1"
    ):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.source_dir = Path(source_dir)
        self.location = location

        # Initialize GCS client
        try:
            self.storage_client = storage.Client(project=project_id)
        except Exception as e:
            print(f"ERROR: Failed to initialize GCS client: {e}")
            print("\nPlease ensure:")
            print("1. GOOGLE_CLOUD_PROJECT environment variable is set")
            print("2. gcloud auth application-default login is completed")
            print("3. Storage API is enabled")
            sys.exit(1)

        self.bucket = None
        self.upload_manifest = {
            "upload_date": datetime.utcnow().isoformat(),
            "project_id": project_id,
            "bucket_name": bucket_name,
            "location": location,
            "files_uploaded": [],
            "statistics": {}
        }

    def create_bucket_if_not_exists(self) -> bool:
        """Create GCS bucket if it doesn't exist."""
        print(f"\n🪣  Checking bucket: gs://{self.bucket_name}")

        try:
            self.bucket = self.storage_client.get_bucket(self.bucket_name)
            print(f"   ✓ Bucket already exists")
            return True
        except exceptions.NotFound:
            print(f"   Creating new bucket...")
            try:
                self.bucket = self.storage_client.create_bucket(
                    self.bucket_name,
                    location=self.location
                )
                print(f"   ✓ Bucket created: gs://{self.bucket_name}")
                print(f"   Location: {self.location}")
                return True
            except exceptions.Conflict:
                print(f"   ✗ Bucket name already taken globally")
                return False
            except Exception as e:
                print(f"   ✗ Failed to create bucket: {e}")
                return False
        except Exception as e:
            print(f"   ✗ Error checking bucket: {e}")
            return False

    def upload_file(self, local_path: Path, gcs_path: str) -> Optional[Dict[str, Any]]:
        """Upload a single file to GCS."""
        try:
            blob = self.bucket.blob(gcs_path)

            # Set content type based on file extension
            content_type = self._get_content_type(local_path)
            blob.content_type = content_type

            # Upload file
            blob.upload_from_filename(str(local_path))

            # Get file metadata
            file_size = local_path.stat().st_size

            file_info = {
                "local_path": str(local_path),
                "gcs_path": f"gs://{self.bucket_name}/{gcs_path}",
                "size_bytes": file_size,
                "content_type": content_type,
                "upload_status": "success"
            }

            print(f"   ✓ Uploaded: {gcs_path} ({self._format_bytes(file_size)})")
            return file_info

        except Exception as e:
            print(f"   ✗ Failed to upload {local_path}: {e}")
            return {
                "local_path": str(local_path),
                "gcs_path": f"gs://{self.bucket_name}/{gcs_path}",
                "upload_status": "failed",
                "error": str(e)
            }

    def upload_directory(self) -> bool:
        """Upload entire knowledge corpus directory to GCS."""
        print(f"\n📤 Uploading knowledge corpus from: {self.source_dir}")

        if not self.source_dir.exists():
            print(f"   ✗ Source directory not found: {self.source_dir}")
            return False

        # Find all files
        files_to_upload = []
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file():
                # Skip git directories and hidden files
                if ".git" not in file_path.parts and not file_path.name.startswith("."):
                    files_to_upload.append(file_path)

        total_files = len(files_to_upload)
        print(f"   Found {total_files} files to upload")

        # Upload files
        successful_uploads = 0
        failed_uploads = 0

        for i, file_path in enumerate(files_to_upload, 1):
            # Calculate relative path for GCS
            relative_path = file_path.relative_to(self.source_dir.parent)
            gcs_path = str(relative_path).replace("\\", "/")

            print(f"\n   [{i}/{total_files}] Uploading: {file_path.name}")

            file_info = self.upload_file(file_path, gcs_path)

            if file_info:
                self.upload_manifest["files_uploaded"].append(file_info)
                if file_info.get("upload_status") == "success":
                    successful_uploads += 1
                else:
                    failed_uploads += 1

        print(f"\n   ✓ Upload complete: {successful_uploads} succeeded, {failed_uploads} failed")
        return failed_uploads == 0

    def verify_uploads(self) -> bool:
        """Verify all files were uploaded successfully."""
        print(f"\n🔍 Verifying uploads...")

        total_files = len(self.upload_manifest["files_uploaded"])
        successful = len([f for f in self.upload_manifest["files_uploaded"]
                         if f.get("upload_status") == "success"])

        print(f"   Total files: {total_files}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {total_files - successful}")

        if successful == total_files:
            print(f"   ✓ All files uploaded successfully")
            return True
        else:
            print(f"   ⚠ Some files failed to upload")
            return False

    def generate_manifest(self) -> bool:
        """Generate upload manifest."""
        print(f"\n📋 Generating upload manifest...")

        # Calculate statistics
        successful_files = [f for f in self.upload_manifest["files_uploaded"]
                          if f.get("upload_status") == "success"]

        total_size = sum(f.get("size_bytes", 0) for f in successful_files)

        self.upload_manifest["statistics"] = {
            "total_files_attempted": len(self.upload_manifest["files_uploaded"]),
            "successful_uploads": len(successful_files),
            "failed_uploads": len(self.upload_manifest["files_uploaded"]) - len(successful_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "bucket_url": f"gs://{self.bucket_name}"
        }

        # Save manifest locally
        manifest_file = self.source_dir / "upload_manifest.json"
        manifest_file.write_text(json.dumps(self.upload_manifest, indent=2))
        print(f"   ✓ Saved locally: {manifest_file}")

        # Upload manifest to GCS
        self.upload_file(
            manifest_file,
            f"{self.source_dir.name}/upload_manifest.json"
        )

        # Also save to outputs
        output_manifest = Path("/mnt/user-data/outputs/03_upload_manifest.json")
        output_manifest.parent.mkdir(parents=True, exist_ok=True)
        output_manifest.write_text(json.dumps(self.upload_manifest, indent=2))
        print(f"   ✓ Saved to outputs: {output_manifest}")

        return True

    def _get_content_type(self, file_path: Path) -> str:
        """Determine content type based on file extension."""
        extension_map = {
            ".json": "application/json",
            ".md": "text/markdown",
            ".txt": "text/plain",
            ".html": "text/html",
            ".py": "text/x-python",
            ".yaml": "text/yaml",
            ".yml": "text/yaml",
        }
        return extension_map.get(file_path.suffix.lower(), "application/octet-stream")

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human-readable string."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB"

    def run(self) -> bool:
        """Execute the complete upload process."""
        print("=" * 70)
        print("ADK KNOWLEDGE CORPUS - GCS UPLOAD (PHASE 2)")
        print("=" * 70)
        print(f"Project: {self.project_id}")
        print(f"Bucket: gs://{self.bucket_name}")
        print(f"Location: {self.location}")

        try:
            # Step 1: Create/check bucket
            if not self.create_bucket_if_not_exists():
                return False

            # Step 2: Upload directory
            if not self.upload_directory():
                print("\n⚠ Some uploads failed, but continuing...")

            # Step 3: Verify uploads
            self.verify_uploads()

            # Step 4: Generate manifest
            self.generate_manifest()

            # Final summary
            print("\n" + "=" * 70)
            print("✅ GCS UPLOAD COMPLETE")
            print("=" * 70)
            stats = self.upload_manifest["statistics"]
            print(f"Bucket: gs://{self.bucket_name}")
            print(f"Files uploaded: {stats['successful_uploads']}/{stats['total_files_attempted']}")
            print(f"Total size: {stats['total_size_mb']} MB")
            print(f"Failed uploads: {stats['failed_uploads']}")
            print("\nNext step: Create Gemini File Search corpus (Phase 3)")
            print("=" * 70)

            return stats['failed_uploads'] == 0

        except Exception as e:
            print(f"\n❌ ERROR: Upload failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("ERROR: GOOGLE_CLOUD_PROJECT environment variable not set")
        print("\nSet it with:")
        print("  export GOOGLE_CLOUD_PROJECT='your-project-id'")
        sys.exit(1)

    # Generate bucket name
    bucket_name = f"mapache-adk-knowledge-{project_id}"

    # Optional: Override bucket name
    if len(sys.argv) > 1:
        bucket_name = sys.argv[1]

    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    print(f"Configuration:")
    print(f"  Project ID: {project_id}")
    print(f"  Bucket: {bucket_name}")
    print(f"  Location: {location}")
    print()

    # Create uploader and run
    uploader = GCSKnowledgeUploader(
        project_id=project_id,
        bucket_name=bucket_name,
        location=location
    )

    success = uploader.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
