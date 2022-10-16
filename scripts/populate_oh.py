import requests

def insert_oh_entry(class_id, oh_id, timestamp, wait_time, num_open_tickets, num_tas_online, num_people_online):
    url = "http://127.0.0.1:5000/oh"
    json_args = {
            'class_id'         : class_id,
            'oh_id'            : oh_id,
            'timestamp'        : timestamp,
            'wait_time'        : wait_time,
            'num_open_tickets' : num_open_tickets,
            'num_tas_online'   : num_tas_online,
            'num_people_online': num_people_online,
    }
    response = requests.post(url, json=json_args)
    return response

def get_num_open_tickets(index, total):
    if (index / total < 0.2):
        return index // 3
    return int(0.3*total) // 3

def get_num_people_online(index, total):
    if (index / total < 0.2):
        return index // 2
    return int(0.2*total) // 2

def get_wait_time(num_open_tickets, num_tas_online):
    avg_ticket_time = 10
    return num_open_tickets * avg_ticket_time // num_tas_online

def generate_oh_entries(class_id, oh_id, date, start_time, end_time):
    hms_array = start_time.split(":")
    start_hour = int(hms_array[0])
    start_min = int(hms_array[1])
    start_sec = int(hms_array[2])

    hms_array = end_time.split(":")
    end_hour = int(hms_array[0])
    end_min = int(hms_array[1])
    end_sec = int(hms_array[2])

    current_hour = start_hour
    current_min = start_min
    timestamps = []
    while (current_hour < end_hour):
        while (current_min < 60):
            if (current_min < 10):
                timestamp = date + " {}:0{}:00".format(current_hour, current_min)
            else:
                timestamp = date + " {}:{}:00".format(current_hour, current_min)
            timestamps.append(timestamp)
            current_min += 1
        current_hour += 1
        current_min = 0
        
    num_open_tickets_arr = []
    num_tas_online_arr = []
    num_people_online_arr = []
    wait_time_arr = []
    for i in range(len(timestamps)):
        timestamp = timestamps[i]
        num_open_tickets = get_num_open_tickets(i, len(timestamps))
        num_open_tickets_arr.append(num_open_tickets)
        num_tas_online = 1
        num_tas_online_arr.append(num_tas_online)
        num_people_online = get_num_people_online(i, len(timestamps))
        num_people_online_arr.append(num_people_online)
        wait_time = get_wait_time(num_open_tickets, num_tas_online)
        wait_time_arr.append(wait_time)
        insert_oh_entry(class_id, oh_id, timestamp, wait_time, num_open_tickets, num_tas_online, num_people_online)
            
generate_oh_entries("cs162", 42, "2022-10-21", "14:00:00", "16:00:00")
