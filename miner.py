import pty
import sys
import os
import time
import subprocess
import logging
import random
import socket
import multiprocessing
import datetime
import psutil

version = "0.1a"

config = os.environ
CONFIG_FILE = '/root/automation/.env'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as fd:
        for line in fd:
            key, value = line.split('=')
            config[key.strip()] = value.strip()

# DO NOT FORGET TO PUT YOUR WALLETS HERE
wallet_list = [config['MINER_WALLET']]

# DO NOT FORGET TO PUT ALARMER KEY HERE
# @alarmer_bot / https://alarmerbot.ru/
alarmer_key = "574d55-db5081-0d7d70"

# The small ones
giver1 = ["kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN",
          "kf8SYc83pm5JkGt0p3TQRkuiM58O9Cr3waUtR9OoFq716lN-",
          "kf-FV4QTxLl-7Ct3E6MqOtMt-RGXMxi27g4I645lw6MTWraV",
          "kf_NSzfDJI1A3rOM0GQm7xsoUXHTgmdhN5-OrGD8uwL2JMvQ",
          "kf9iWhwk9GwAXjtwKG-vN7rmXT3hLIT23RBY6KhVaynRrIK7"
          ]

# The big ones
giver2 = [
    "kf8guqdIbY6kpMykR8WFeVGbZcP2iuBagXfnQuq0rGrxgE04",
    "kf9CxReRyaGj0vpSH0gRZkOAitm_yDHvgiMGtmvG-ZTirrMC",
    "kf-WXA4CX4lqyVlN4qItlQSWPFIy00NvO2BAydgC4CTeIUme",
    "kf8yF4oXfIj7BZgkqXM6VsmDEgCqWVSKECO1pC0LXWl399Vx",
    "kf9nNY69S3_heBBSUtpHRhIzjjqY0ChugeqbWcQGtGj-gQxO",
    "kf_wUXx-l1Ehw0kfQRgFtWKO07B6WhSqcUQZNyh4Jmj8R4zL",
    "kf_6keW5RniwNQYeq3DNWGcohKOwI85p-V2MsPk4v23tyO3I",
    "kf_NSPpF4ZQ7mrPylwk-8XQQ1qFD5evLnx5_oZVNywzOjSfh",
    "kf-uNWj4JmTJefr7IfjBSYQhFbd3JqtQ6cxuNIsJqDQ8SiEA",
    "kf8mO4l6ZB_eaMn1OqjLRrrkiBcSt7kYTvJC_dzJLdpEDKxn"
]

logfile = "app.log"

conf = "/var/lite-client/ton-lite-client-test1.config.json"
db = "/var/lite-client/ton-db-dir"
liteclient = "/root/ton-build/lite-client/lite-client"
miner = "/root/ton-build/crypto/pow-miner"
pow_result = "/var/lite-client/mined.boc"

blocks_log_dir = "/var/lite-client/blocks/"

cores = "-w " + str(multiprocessing.cpu_count())
timeout = "-t 43200"
iterations = "100000000000"

hostname = str(socket.gethostname())

# Global useful vars
r = 0

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def send_alarmer(text):
	pass
#     try:
#         parsed = urllib.parse.quote_plus(hostname + " - " + text)
#         r = requests.get('https://alarmerbot.ru/?key=' + alarmer_key + '&message=' + parsed)
#         if r.status_code != 200:
#             logging.info("Error sending update via alarmer. Response=" + str(r.status_code))
#     except:
#         logging.info("Error sending update via alarmer. Exception appeared")


def get_rand_wallet():
    return (random.choice(wallet_list))


def count_block():
    try:
        filename1 = datetime.datetime.now().strftime("%Y%m%d")
        if os.path.exists(blocks_log_dir + filename1):
            f = open(blocks_log_dir + filename1, "r")
            old = int(f.readline())
            f.close()
            new = old + 1
            f = open(blocks_log_dir + filename1, "w")
            f.write(str(new))
            f.close()
        else:
            f = open(blocks_log_dir + filename1, "w")
            f.write("1")
            f.close()
        logging.info("Counted block into block log")
    except:
        logging.info("ERROR - Can't count block")


def get_from_chain(given_giver):
    try:
        filepath = os.path.join('/tmp', 'liteclient_%s' % given_giver)
        os.system(
            liteclient + ' -vv -C ' + conf + ' -D ' + db + ' -c "runmethod ' + given_giver + ' get_pow_params" > %s' % filepath)
        file = open(filepath)
        all_lines = file.readlines()
        result = all_lines[6].split()
        seed = result[2]
        complexity = result[3]
        os.remove(filepath)
        return (seed, complexity)
    except:
        return (0, 0)


if multiprocessing.cpu_count() <= 128:
    giver = giver1
    logging.info("CPU is " + str(multiprocessing.cpu_count()) + " cores, going with small givers")
    send_alarmer("CPU is " + str(multiprocessing.cpu_count()) + " cores, going with small givers")
else:
    giver = giver2
    logging.info("CPU is " + str(multiprocessing.cpu_count()) + " cores, going with big givers")
    send_alarmer("CPU is " + str(multiprocessing.cpu_count()) + " cores, going with big givers")


def get_hashes_needed(giver4check):
    temp_data = get_from_chain(giver4check)
    temp_wallet = "kf9T0nvBcv5kIVN5A9c0tW0pD5Cy2PpBNy6NjXXulzMGEiTD"
    args = [miner, '-vv'] + cores.split()
    boc_result = os.path.join('/tmp', 'tmp_mined_%s.boc' % giver4check)
    args += ['-t', '1', temp_wallet, temp_data[0], temp_data[1], iterations, giver4check, boc_result]
    args = [str(x) for x in args]
    checkproc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = str(checkproc.stdout.readline())
    out = out.split()

    return (giver4check, out[6])


def get_rand_giver():
    b = datetime.datetime.now()
    hash_dict = {}
    with multiprocessing.Pool(8) as p:
        res = p.map(get_hashes_needed, giver)
        hash_dict = {x: y for x, y in res}
    print(datetime.datetime.now() - b)
    try:
        index = len(giver)
        for n_giver in giver:
            hashes = int(hash_dict[n_giver])
            if index == len(giver):
                giver_result = n_giver + " " + str(hashes)
                logging.info(str(index) + " " + giver_result)
                index = index - 1
            else:
                logging.info(str(index) + " " + n_giver + " " + str(hashes))
                temp_result = giver_result.split()
                if int(temp_result[1]) >= hashes:
                    giver_result = n_giver + " " + str(hashes)
                index = index - 1
        for proc in psutil.process_iter():
            if proc.name() == "pow-miner":
                proc.kill()
        check_results = giver_result.split()
        logging.info("Result = " + giver_result)
        send_alarmer("Choosing the easiest giver - " + giver_result)
        return check_results[0]
    except:
        logging.exception("Fucked up with choosing the easiest, going with rand")
        send_alarmer("Fucked up with choosing the easiest, going with rand")
        return (random.choice(giver))


def main():
    # MAIN CYCLE
    while True:
        i = 0

        filename_temp = datetime.datetime.now().strftime("%Y%m%d")
        if not os.path.exists(blocks_log_dir + filename_temp):
            f = open(blocks_log_dir + filename_temp, "w")
            f.write("0")
            f.close()

        if os.path.exists(pow_result):
            os.remove(pow_result)
        if os.path.exists("tmp"):
            os.remove("tmp")

        for proc in psutil.process_iter():
            if proc.name() == "pow-miner":
                proc.kill()

        wallet = get_rand_wallet()
        logging.info("Chose wallet - " + str(wallet))

        temp_giver = get_rand_giver()

        logging.info("Giver for this round - " + temp_giver)

        data = get_from_chain(temp_giver)
        if data[0] != 0:
            minerproc = subprocess.Popen([miner, '-vv', cores, timeout, wallet, data[0], data[1], iterations,
                                          temp_giver, pow_result], shell=False, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
            if minerproc.poll() != None:
                logging.info("Miner didn't start. Exiting")
                send_alarmer("Miner didn't start. Exiting")
                exit(10)
            else:
                out = str(minerproc.stdout.readline())
                out = out.split()
                compl = data[1]
                hashes = str(out[6])
                logging.info("Started miner with pid=" + str(minerproc.pid) + ", giver=" + temp_giver + ", seed=" + data[
                    0] + ", compl=" + compl + ", hashes=" + hashes)
                send_alarmer("Started miner for wallet " + wallet)
                with open(logfile, 'a') as the_file:
                    the_file.write(str(datetime.datetime.now()) + ';' + str(temp_giver) + ';' + str(data[0]) + ';' + str(
                        data[1]) + ';' + str(out[6]) + '\n')
                    the_file.close()
                while i == 0:
#                    time.sleep(5)
                    data2 = get_from_chain(temp_giver)
                    if data2[0] != data[0]:
                        minerproc.kill()
                        logging.info("Seed changed. Restarting miner")
                        send_alarmer("Seed changed. Restarting miner")
                        i = i + 1
                    else:
                        if minerproc.poll() == 0:
                            os.system(liteclient + ' -vv -C ' + conf + ' -D '
                                      + db + ' -c "sendfile ' + pow_result + '" > send_result')
                            logging.info("Block found for wallet " + str(wallet))
                            send_alarmer("Block found for wallet " + str(wallet))
                            count_block()
                            if os.path.exists(pow_result):
                                os.remove(pow_result)
                            i = i + 1
                            time.sleep(2)
                        else:
                            if minerproc.poll() == None:
                                logging.info("Seed still the same")
                            else:
                                logging.info("Miner failed with exitcode=" + str(minerproc.poll()))
                                logging.info("Restarting miner")
                        if os.path.exists(pow_result):
                            logging.info("Something strange - there are pow result file exist")
        else:
            logging.info("Can't get POW params from chain, retry in 60 seconds")
            send_alarmer("Can't get POW params from chain, retry in 60 seconds")
            time.sleep(60)


def daemon():
    cwd = config.get('MINER_CWD')
    if cwd:
        os.chdir(cwd)

    try:
        pid = os.fork()
        if pid > 0:
            exit(0)
    except OSError as e:
        logging.exception('fail to fork')
        exit(1)

    pid, fd = pty.fork()
    sys.stdout.flush()
    sys.stderr.flush()
    new_stdout = open('stdout.txt', 'w')
    new_stderr = open('stderr.txt', 'w')
    os.dup2(new_stdout.fileno(), 1)
    os.dup2(new_stderr.fileno(), 2)

    if pid != 0:
        with open('.ppid', 'w') as fd:
            fd.write('%s\n' % os.getpid())

        os.waitpid(pid, 0)
        return

    with open('.pid', 'w') as fd:
        fd.write('%s\n' % os.getpid())

    main()


if '__main__' == __name__:
    # daemon()
    main()
