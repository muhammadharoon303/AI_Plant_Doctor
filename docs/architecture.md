# System Architecture - AI Plant Doctor

The AI Plant Doctor platform is designed as a decoupled, multi-tiered enterprise architecture separating the mobile client, REST backend services, database schema, and PyTorch AI computer vision pipeline.

## System Architecture Diagram

```
+-------------------------------------------------------------+
|                      Flutter Mobile App                     |
|         (Material 3, i18n English/Urdu/Pashto, RTL)         |
+------------------------------+------------------------------+
                               | HTTPS / JSON & Multipart
                               v
+-------------------------------------------------------------+
|                     FastAPI Backend REST                    |
|      (JWT Auth, Pydantic Validation, Routers v1)            |
+---------------+------------------------------+--------------+
                |                              |
                v                              v
+---------------+---------------+  +-----------+--------------+
|     PostgreSQL / SQLAlchemy   |  |   PyTorch AI CV Engine   |
|   (Users, Diseases, Scans)    |  | (ResNet + U-Net Lesion)  |
+-------------------------------+  +--------------------------+
```

## AI Computer Vision Model Decoupling Strategy

1. **API Abstraction**: The Flutter client and external callers consume a standardized `POST /api/v1/diagnose` contract.
2. **PyTorch Engine Wrapper**: The backend invokes `PlantDoctorAIEngine.predict(image_bytes)`.
3. **Plug-and-Play Upgrades**: The PyTorch CNN classification backbone or U-Net segmentation model can be replaced with custom trained weights, ONNX, or TensorRT runtimes without modifying API parameters or client code.
