import multiprocessing

#   Project name amd url
projectName = "boston"
mainUrl = "https://www.boston.com/"

#   Thread amount equals double of processor amount
numberOfThreads = multiprocessing.cpu_count() * 2

#   group of words separated by ','
wordsToSearch = "island,NBA"

#   flag to stop working
max_links = 200
