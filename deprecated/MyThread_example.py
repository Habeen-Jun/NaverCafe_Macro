
class MyThread(QThread):
    """
    스레드 멈추는 함수 만들기 전 임시로 썼던 클래스.
    혹시 몰라서 따로 빼둠..
    main에서 객체생성 후 호출 되는 녀석.
    """
    def __init__(self,window):
        self.window = window
        QThread.__init__(self)
        print("worker thread created!")

    def job(self,naver,total_interval,interval,option_data, item_list):
        self.stop_event = threading.Event()
        naver.post(interval, option_data, item_list)
        while not self.stop_event.is_set():
            self.t = threading.Timer(total_interval,self.job, args=(naver,total_interval,interval,option_data,item_list))
            self.t.start()
            self.t.join()
            self.window.textBrowser.append('작업종료')
            
    def do_job_once(self, naver, interval, option_data, item_list):
        naver.post(interval, option_data, item_list)
    def stop(self):
        self.stop_event = threading.Event()
        # Tell the thread to stop...
        self.stop_event.set()
        # Wait for the thread to stop
        # self.t.join()
        print("thread stopped")


def main(naver,total_interval,interval,option_data,item_list):
    mt = MyThread()
    if total_interval == 0:
        mt.do_job_once(naver,interval,option_data,item_list)
    else:
        mt.job(naver,total_interval,interval,option_data,item_list)