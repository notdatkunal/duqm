from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


# csilms = ConnectionsElement.get_csilms().app_session
#


# @scheduler.scheduled_job('interval', seconds=60 * 60 * 4)
@scheduler.scheduled_job('interval', seconds=60 * 30)
def gatepass_schedulings_data():
    print('gatepass schedulings saved')


@scheduler.scheduled_job('interval', seconds=60 * 60)
def gatepass_batch_insert():
    ...


@scheduler.scheduled_job('interval', seconds=60 * 30)
def srv_schedulings_data():
    print('this is srv schedulings')


@scheduler.scheduled_job('interval', seconds=60 * 60)
def srv_batch_insert():
    ...


@scheduler.scheduled_job('interval', seconds=60 * 30)
def schedulings_manager():
    print("scheduled task started")
    second_of_the_month_check = date.today().day >= 2
    seventh_of_the_month_check = date.today().day >= 7
    if seventh_of_the_month_check:
        pass
    # UNCOMMENT CODE FROM THIS FUNCTION

    if second_of_the_month_check:
        pass
    try:
        ...
        # create_gatepass_schedules()
    except Exception as e:
        print("error in gatepass")
        print(e)
    try:
        ...
        # create_receipt_schedules()
    except Exception as e:
        print("error in srv")
        print(e)
    print("scheduled task completed")

#
# #
# # def check_generated_schedulings_on_running_month() -> bool:
# #     """
# #     select count(*) from Scheduling where  datename(month, current_date()) = datename(month, DateTimeGenerated)
# #     :return:
# #     """
# #     return (csilms.query(func.count().label('Count'))
# #             .select_from(IVMS_Scheduling)
# #             .filter(func.month(IVMS_Scheduling.DateTimeGenerated) == date.today().month)
# #             .first().Count < 1)
