
import frappe
import pandas as pd
import io
import base64

@frappe.whitelist()
def upload_and_calculate(filedata):
    try:
        # Decode and read Excel
        content = base64.b64decode(filedata)
        xls = pd.ExcelFile(io.BytesIO(content))

        materials_df = xls.parse("Materials")
        elements = [
            "Footings & Slabs", "Foundation Walls", "Structural Elements",
            "Ext. Walls", "Party Walls", "Cladding", "Windows", "Int. Walls",
            "Floors", "Ceilings", "Roof", "Garage"
        ]

        total_emissions = 0.0
        details = []

        for sheet in elements:
            try:
                df = xls.parse(sheet, skiprows=3)
                df = df.dropna(subset=["Unnamed: 13"], how="all")
                for _, row in df.iterrows():
                    material_id = row.get("Unnamed: 13")
                    quantity = row.get("Unnamed: 8")
                    if pd.isna(material_id) or pd.isna(quantity):
                        continue

                    match = materials_df[materials_df["ID"] == material_id]
                    if not match.empty:
                        factor = match["GWP kgCO2e/(common unit)"].values[0]
                        try:
                            emissions = float(str(quantity).replace(",", "")) * float(factor)
                            total_emissions += emissions
                            details.append(f"{material_id}: {emissions:.2f} kg CO₂e")
                        except:
                            continue
            except:
                continue

        return {
            "total_emissions": round(total_emissions, 2),
            "details": details
        }

    except Exception as e:
        return {"error": str(e)}
