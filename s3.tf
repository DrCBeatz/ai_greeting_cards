# s3.tf

resource "aws_s3_bucket" "media_bucket" {
    bucket = "ai-greeting-cards-media"

    # Other bucket settings if any...
}

resource "aws_s3_bucket_public_access_block" "media_bucket_public_access" {
  bucket                  = aws_s3_bucket.media_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "media_bucket_policy" {
  bucket = aws_s3_bucket.media_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.media_bucket_public_access] # Ensure public access block is configured first

  policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::ai-greeting-cards-media/*"
        }
      ]
    }
  EOF
}

resource "aws_s3_bucket_versioning" "media_bucket_versioning" {
  bucket = aws_s3_bucket.media_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "media_bucket_cors" {
  bucket = aws_s3_bucket.media_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["*"]
  }
}
