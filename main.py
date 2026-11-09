from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Database Tables Auto-Create කිරීම
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database එකට කතා කරන්න Session එකක් ගන්න function එක
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AutoRescue API is Running Successfully!"}

# 1. අලුත් Mechanic කෙනෙක් Database එකට Save කරන Endpoint එක (POST)
@app.post("/mechanics")
def create_mechanic(mechanic: schemas.MechanicCreate, db: Session = Depends(get_db)):
    # Database Model එකට අදාළව අලුත් Mechanic කෙනෙක් හදනවා
    new_mechanic = models.Mechanic(name=mechanic.name, skill=mechanic.skill, distance=mechanic.distance)
    # එයාගේ විස්තර DB එකට Save කරනවා
    db.add(new_mechanic)
    db.commit()
    db.refresh(new_mechanic)
    return {"message": "Mechanic saved successfully!", "data": new_mechanic}

# 2. Database එකේ ඉන්න ඔක්කොම Mechanics ලා බලන Endpoint එක (GET)
@app.get("/mechanics")
def get_all_mechanics(db: Session = Depends(get_db)):
    # DB එකේ mechanics table එකේ තියෙන ඔක්කොම දත්ත අරන් එනවා
    all_mechanics = db.query(models.Mechanic).all()
    return {"mechanics_online": len(all_mechanics), "data": all_mechanics}

# 3. Mechanic කෙනෙක්ව Database එකෙන් මකලා දාන Endpoint එක (DELETE)
@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    # මුලින්ම බලනවා ඒ ID එකට අදාළ mechanic කෙනෙක් DB එකේ ඉන්නවද කියලා
    mechanic_to_delete = db.query(models.Mechanic).filter(models.Mechanic.id == mechanic_id).first()
    
    if not mechanic_to_delete:
        return {"error": "Mechanic not found!"}
    
    # ඉන්නවා නම් එයාව මකලා දානවා
    db.delete(mechanic_to_delete)
    db.commit()
    return {"message": f"Mechanic with ID {mechanic_id} deleted successfully!"}

# 4. Mechanic කෙනෙක්ගේ විස්තර අලුත් කරන Endpoint එක (PUT)
@app.put("/mechanics/{mechanic_id}")
def update_mechanic(mechanic_id: int, updated_data: schemas.MechanicCreate, db: Session = Depends(get_db)):
    # මුලින්ම බලනවා DB එකේ ඒ ID එකට අදාළ mechanic ඉන්නවද කියලා
    mechanic = db.query(models.Mechanic).filter(models.Mechanic.id == mechanic_id).first()
    
    if not mechanic:
        return {"error": "Mechanic not found!"}
    
    # ඉන්නවා නම් අලුත් විස්තර ටික DB එකට දානවා
    mechanic.name = updated_data.name
    mechanic.skill = updated_data.skill
    mechanic.distance = updated_data.distance
    
    # අලුත් කරපු දත්ත ටික DB එකේ Save කරනවා
    db.commit()
    db.refresh(mechanic)
    return {"message": "Mechanic updated successfully!", "data": mechanic}
