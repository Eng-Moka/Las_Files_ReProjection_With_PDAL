import os
import json
import pdal

# =========================================
# المجلدات
# =========================================
input_folder = r"D:\LAS_Files"

geoid_raster = r"Geoid_KSA21_EPSG_9358.tif"

output_folder = r"D:\LAS_Output"

# إنشاء مجلد الإخراج إذا غير موجود
os.makedirs(output_folder, exist_ok=True)

# =========================================
# المرور على جميع ملفات LAS
# =========================================
for file_name in os.listdir(input_folder):

    # التأكد أن الملف LAS أو LAZ
    if file_name.lower().endswith((".las", ".laz")):

        input_las = os.path.join(input_folder, file_name)

        # اسم ملف الإخراج
        output_las = os.path.join(
            output_folder,
            os.path.splitext(file_name)[0] + "_GRF17_Geoid21.las"
        )

        print("\n=================================")
        print(f"Processing: {file_name}")
        print("=================================")

        # =========================================
        # Pipeline
        # =========================================
        pipeline_json = {
            "pipeline": [

                {
                    "type": "readers.las",
                    "filename": input_las
                },

                {
                    "type": "filters.reprojection",
                    "in_srs": "EPSG:32638",
                    "out_srs": "EPSG:9358"
                },

                {
                    "type": "filters.hag_dem",
                    "raster": geoid_raster
                },

                {
                    "type": "filters.assign",
                    "value": "Z = HeightAboveGround"
                },

                {
                    "type": "writers.las",
                    "filename": output_las
                }

            ]
        }

        try:

            # تشغيل PDAL
            pipeline = pdal.Pipeline(
                json.dumps(pipeline_json)
            )

            pipeline.execute()

            print("Success")
            print(f"Output: {output_las}")

        except Exception as e:

            print("Failed")
            print(e)

print("\n=================================")
print("All Files Processed")
print("=================================")