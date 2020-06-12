import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import time
import params

HOMEPAGE = params.mainUrl
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = params.projectName + '/queue.txt'
CRAWLED_FILE = params.projectName + '/crawled.txt'
queue = Queue(params.max_links)
Spider(params.projectName, HOMEPAGE, DOMAIN_NAME)
links_found = 0
threads = list()


#   Complete task with threads
def create_workers():
    global threads
    for index in range(params.numberOfThreads):
        threads.append(threading.Thread(target=work, daemon=True))
        threads[index].start()


# Do the next job in the queue
def work():
    global links_found
    #   While not reaching link limit
    while queue.qsize() < params.max_links:
        #   Grab the links from file
        queued_links = file_to_set(QUEUE_FILE)
        links_found = len(queued_links)

        #   Take a link and crawl it
        url = queue.get()
        start_crawl_time = time.time()
        Spider.crawl_page(threading.current_thread().name, url)
        end_crawl_time = time.time()

        #   Log the task time
        with open(params.projectName + '/timeLog.txt', 'a') as file:
            file.write(threading.current_thread().name + ": " + str(
                round(end_crawl_time - start_crawl_time, 2)) + ' seconds\n')

        #   Flag the queue that a task is done
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    #   Put all the links from the file in the queue
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    #   If queue reached the setting's limit
    if queue.qsize() >= params.max_links:
        #   Clear queue to signal work is done
        queue.queue.clear()
    else:
        #   Wait for all tasks to be done
        queue.join()

    #   Repeat over the process
    crawl()


def crawl():
    #   Grab the links
    global links_found
    queued_links = file_to_set(QUEUE_FILE)

    #   If we havent reached the link limit
    if len(queued_links) > 0 and links_found < params.max_links:
        #   Start crawling
        create_jobs()


print(f"Running with {params.numberOfThreads} threads")
start_time = time.time()
#   Start work with threads
create_workers()
#   Check more work
crawl()
end_time = time.time()
print(f"Task completed in {str(round(end_time - start_time, 2))} seconds")
