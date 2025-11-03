import csv

with open('FOB_Itemdetails_Final_CSV.csv', 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    master_string = """
        
        
    """
    master_dict = {}
    for row in csv_reader:
        string_q = f"""
        INSERT INTO public.fob_item(
	item_code, section_head, item_desc, country_code, item_deno, months_shelf_life, crp_category, ved_category, abc_category, date_time_approved, approved_by, review_sub_section_code, incatyn)
	VALUES (\'{row['ItemCode']}\', \'{row['SectionHead']}\', \'{row['ItemDesc']}\', \'{'null' if len(row['CountryCode']) == 0 else row['CountryCode']}\', \'{'null' if len(row['ItemDeno']) == 0 else row['ItemDeno']}\', \'{'null' if len(row['MonthsShelfLife']) == 0 else row['MonthsShelfLife']}\', \'{'null' if len(row['CRPCategory']) == 0 else row['CRPCategory']}\', \'{'null' if len(row['VEDCategory']) == 0 else row['VEDCategory']}\', \'{row['ABCCategory']}\', null, \'{row['ApprovedBy']}\', \'{row['ReviewSubSectionCode']}\', \'{row['INCATYN']}\');
        
        
        """
        master_dict = {row['ItemCode']: string_q}
    for item in master_dict.values():
        master_string += item
    with open('item_code.sql', 'w') as file:
        file.write(master_string)
