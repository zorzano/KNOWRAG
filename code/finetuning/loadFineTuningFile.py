from openai import OpenAI
import argparse

# According to https://platform.openai.com/docs/api-reference/files and https://platform.openai.com/docs/guides/fine-tuning
client = OpenAI()

parser = argparse.ArgumentParser(
                    prog='loadFileTuningFile',
                    description='File uploader for model fine tuning',
                    epilog='Knowledge and Things')
                    
parser.add_argument('-a', dest="action", help="action=[load|listfiles|deletefile|finetune|list|retrieve|events|cancel|delete|listmodels")
parser.add_argument('filename', help="Name of json file, or job identifier")

args = parser.parse_args()

if args.action == "load" :
    r=client.files.create(
        file=open(args.filename, "rb"),
        purpose="fine-tune"
    )
    print(r)
    exit()

if args.action == "listfiles":
    r=client.files.list()
    print(r)
    exit()

if args.action == "deletefile":
    r=client.files.delete(args.filename)
    print(r)
    exit()

if args.action == "finetune":
    r=client.fine_tuning.jobs.create(
        training_file=args.filename,
        model="gpt-4o-mini-2024-07-18"
    )
    print(r)
    exit()
 

# List 10 fine-tuning jobs
if args.action == "list":
    r=client.fine_tuning.jobs.list(limit=10)
    print(r)
    exit()

# Retrieve the state of a fine-tune
if args.action == "retrieve":
    r=client.fine_tuning.jobs.retrieve(args.filename)
    print(r)
    exit()


# Cancel a job
if args.action == "cancel":
    r=client.fine_tuning.jobs.cancel(args.filename)
    print(r)
    exit()

# List up to 10 events from a fine-tuning job
if args.action == "events":
    r= client.fine_tuning.jobs.list_events(fine_tuning_job_id=args.filename, limit=10)
    print(r)
    exit()

# Delete a fine-tuned model
if args.action == "delete":
    r=client.models.delete(args.filename)
    print(r)
    exit()
    
if args.action == "listmodels":
    r=client.models.list()
    print(r)
    exit()
 