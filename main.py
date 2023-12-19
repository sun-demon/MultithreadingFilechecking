import os
import sys
import time
import threading


class FileChecksumThread(threading.Thread):
    def __init__(self, filename):
        self.filename, self.sum, self.max_progress, self.progress = filename, 0, 0, 0
        threading.Thread.__init__(self)

    def run(self):
        with open(self.filename, 'rb') as file:
            data = file.read()
            self.max_progress = len(data)
            self.progress = 0
            for i in range(len(data)):
                self.sum += data[i]
                self.progress += 1
        if self.max_progress == 0:
            self.max_progress = 1
            self.progress = 1

    def __str__(self):
        max_pieces = 20
        pieces = 0 if self.progress == 0 else self.progress * max_pieces // self.max_progress
        max_integer_digits_number = 12
        str_progress = str(self.progress).rjust(max_integer_digits_number)
        str_max_progress = str(self.max_progress).ljust(max_integer_digits_number)
        result = f'IN PROCESS: |' + '#' * pieces + ' ' * (max_pieces - pieces) + f'| {str_progress} /{str_max_progress}'
        result += f'  checksum: {str(self.sum).rjust(max_integer_digits_number)}  file: {self.filename}'
        if self.progress == self.max_progress and self.progress != 0:
            result = 'COMPLETED ' + result[10:]
        return result


def clear():
    os.system('cls')


def listeners_monitor(files_checksums_threads):
    clear()
    string = '\n'.join([str(thread) for thread in files_checksums_threads])
    print(string)
    while any([thread.is_alive() for thread in files_checksums_threads]):
        string = '\n'.join([str(thread) for thread in files_checksums_threads])
        clear()
        print(string)
        time.sleep(0.02)
    clear()
    print('\n'.join([str(thread) for thread in files_checksums_threads]))


if __name__ == '__main__':
    filenames = sys.argv[1:]
    n = len(filenames)
    threads = [FileChecksumThread(filename) for filename in filenames]
    listeners_printer_thread = threading.Thread(target=listeners_monitor, args=(threads,))
    for i in range(n):
        threads[i].start()
    listeners_printer_thread.start()
    for i in range(n):
        threads[i].join()
    listeners_printer_thread.join()
    time.sleep(2)
