import csv
from fob_sybase.Connections import ConnectionsElement
from fob_sybase.csilms.tables import Item, ItemLine
from sqlalchemy import func

session = ConnectionsElement.get_csilms().app_session

with open('FOB_Itemdetails_Final_CSV.csv', 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    item_codes = [row['ItemCode'] for row in csv_reader]
    print(item_codes)
    query = (session
             .query(ItemLine.ItemCode, ItemLine.SHNo, ItemLine.QtyMSL, ItemLine.QtyUSL, ItemLine.QtyACL,
                    ItemLine.StationCode, ItemLine.QtyWarReserve, ItemLine.DateTimeAdded, ItemLine.DateTimeClosed,
                    ItemLine.DaysLTProc, ItemLine.ItemLineSerial)
             # .join(Item, ItemLine.ItemCode == Item.ItemCode)
             .filter(ItemLine.ItemCode.in_(item_codes))
             )
    master_string = """
    
    """
    for item in query.all():
        string_query = f"""
                    INSERT INTO public.fob_item_line(
	    item_code, station_code, sh_no, qty_war_reserve, qty_msl, qty_usl, qty_acl, days_lt_proc, date_time_added, date_time_closed, item_line_serial)
	VALUES ('{item.ItemCode.strip()}', '{item.StationCode}','{item.SHNo}', '{item.QtyWarReserve}', '{item.QtyMSL}', '{item.QtyUSL}', '{item.QtyACL}', '{item.DaysLTProc}', '{'null' if item.DateTimeAdded is None else item.DateTimeAdded}', '{'null' if item.DateTimeClosed is None else item.DateTimeClosed}', '{item.ItemLineSerial}' );

                """
        print(string_query)
        master_string += string_query
    with open('itemline.sql', 'w') as file:
        file.write(master_string)
