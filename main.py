from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Health Check Service", version="1.0.0")


class Service(BaseModel):
    id: int
    name: str
    status: str  # e.g., "healthy", "unhealthy", "degraded"
    description: str = ""


# In-memory list to simulate a health status store
services: List[Service] = []


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Health Check Service!"}


@app.get("/health", response_model=List[Service], tags=["Health"])
def get_all_services():
    return services


@app.get("/health/{service_id}", response_model=Service, tags=["Health"])
def get_service(service_id: int):
    for service in services:
        if service.id == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found")


@app.post("/health", response_model=Service, tags=["Health"])
def add_service(service: Service):
    if any(s.id == service.id for s in services):
        raise HTTPException(status_code=400, detail="Service with this ID already exists")
    services.append(service)
    return service


@app.put("/health/{service_id}", response_model=Service, tags=["Health"])
def update_service(service_id: int, updated_service: Service):
    for index, service in enumerate(services):
        if service.id == service_id:
            services[index] = updated_service
            return updated_service
    raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/health/{service_id}", response_model=Service, tags=["Health"])
def delete_service(service_id: int):
    for index, service in enumerate(services):
        if service.id == service_id:
            return services.pop(index)
    raise HTTPException(status_code=404, detail="Service not found")
