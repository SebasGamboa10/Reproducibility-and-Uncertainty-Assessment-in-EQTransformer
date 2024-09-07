from glob import glob
from obspy import read_inventory, Inventory

inventory = Inventory()
resp_dir = '/work/sgamboa/oksp/data/Dataless_verificado/Dataless_nodos/TUNEL.dataless'
for fname in glob(resp_dir):
    inv = read_inventory(fname)
    inventory = inventory.__add__(inv)

#inv1 = read_inventory('/work/sgamboa/oksp/data/Dataless_verificado/ovsi2020.dataless')

inv1 = read_inventory('/work/sgamboa/oksp/data/Dataless_verificado/Dataless_nodos/inventory.xml')
inventory = inventory.__add__(inv1)

inventory.write('/work/sgamboa/oksp/data/Dataless_verificado/Dataless_nodos/inventory.xml',
                format='STATIONXML')
