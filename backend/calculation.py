import pandas as pd
from backend.filter_data import filter_desicion



def check_zero(a):

    # notna to find out if value is nan, return false if it is nan
    # return zero if it's empty string or 0
    return str(int(a)) if pd.notna(a) else "0"



# === counting platser for selected organizer anordnare Marcus ===
def count_approved_spots(filtered):

    filtered = filter_desicion(filtered)

    try:
        totala = float(filtered["Totalt antal beviljade platser"].sum())

        return max(totala, 0)

    except Exception as e:
        print("Fel i beräkning:", e)
        return 0
# === end ===


# === count KPI:er for percentage anordnare Marcus=== 
def count_percentage(part, hole):

    try:
        # Percentage for applied courses

        if not part and not hole or str(part).strip() == "" or str(hole).strip() == "":

            return "0%"

        a = int(part)
        b = int(hole)

        if a and b > 0:
            return f"{a/b * 100:.1f}%"

        else:
            return "0%"

    except Exception as e:
        print("Fel count_percentage", e)
        print(f"Fel uträkning")
        print(f"fel Ingen uträkning")
        
# === End ====
