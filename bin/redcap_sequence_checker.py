import redcap
import io
import os
import json
import connect_slack
import schedule
import time

def connect_to_redcap():
    # Connects to and returns project data frame
    # Uses gssotelo Api key
    api_url = 'https://geco.ritm-edc.net/redcap/api/'
    api_key = 'CA7768C863D7E1A5791BC222E92C3A0C'
    project = redcap.Project(api_url, api_key)
    project_df = project.export_records(format='df')
    return project_df

def check_sequence_number(project_df):
    # Return current number of sequences in database
    redcap_consensus_names = [x for x in project_df.consensus.astype(str) if x != "nan"]
    sequence_number = len(redcap_consensus_names)
    return sequence_number

def json_check(filename, latest_sequence_number):
    # Checks if file exists
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        pass
    else:
        directory = os.getcwd()
        with io.open(os.path.join(directory, filename), 'w') as db_file:
            db_file.write(json.dumps({"Current Sequence Number": latest_sequence_number}))
            db_file.close()
        message = f'Restarting count of sequence tally. {latest_sequence_number} sequences are currently uploaded to REDCap'
        connect_slack.slack_post(message)

def json_read(filename):
    # Gets current sequence number from file
    directory = os.getcwd()
    with io.open(os.path.join(directory, filename), 'r') as db_file:
        current_sequence_number = json.load(db_file)
        db_file.close()
        return current_sequence_number

def json_update(filename, log_sequence_number):
    # Updates sequence number in file
    directory = os.getcwd()
    with io.open(os.path.join(directory, filename), 'w') as db_file:
        db_file.write(json.dumps({"Current Sequence Number": log_sequence_number}))
        db_file.close()

def check_and_post_new_sequence():
    #checks and posts number of new sequences
    redcap_projectdf = connect_to_redcap()
    latest_sequence_number = check_sequence_number(redcap_projectdf)

    json_check('current_sequence_number.json', latest_sequence_number)
    sequence_dict = json_read('current_sequence_number.json')
    current_sequence_number = sequence_dict['Current Sequence Number']

    new_sequence_number = latest_sequence_number - current_sequence_number

    if new_sequence_number > 0:
        message = str(new_sequence_number) + ' new sequences uploaded to REDCap'
        connect_slack.slack_post(message)
        json_update('current_sequence_number.json', latest_sequence_number)

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(check_and_post_new_sequence)
    schedule.every().day.at("17:00").do(check_and_post_new_sequence)
    while True:
        n = schedule.idle_seconds()
        print(n)
        time.sleep(n)
        schedule.run_pending()
        
