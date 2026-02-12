import sys
import os
# Add parent directory to path to allow imports from libs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs.ShivaApi import Order

# Init Order client
order_client = Order(
    url="https://shiva.cloud-temple.com",
    token_id="",
    token_secret=""
)

# Get consumptions for a specific period
# Format: YYYY-MM-DD
start_date = "2026-01-15"
end_date = "2026-01-17"

print(f"Récupération des consommations du {start_date} au {end_date}...\n", flush=True)

try:
    consumptions = order_client.get_consumptions(
        start_date=start_date,
        end_date=end_date
    )
    
    print(f"Nombre total de SKU: {len(consumptions)}\n", flush=True)
    print("=" * 80, flush=True)
    
    for item in consumptions:
        usage = item.get('usage')
        sku = item.get('sku', {})
        sku_name = sku.get('name', 'N/A')
        sku_unit = sku.get('unit', 'N/A')
        sku_desc_fr = sku.get('descriptionFr', 'N/A')
        
        print(f"\n📊 SKU: {sku_name}")
        print(f"   Usage: {usage} {sku_unit}")
        print(f"   Description: {sku_desc_fr}")
        print("-" * 80)

except ValueError as e:
    print(f"❌ Erreur de validation: {e}")
except Exception as e:
    print(f"❌ Erreur lors de la récupération des consommations: {e}")
