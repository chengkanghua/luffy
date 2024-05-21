#引入任务
from mycelery.sms.tasks import send_sms
#执行任务
send_sms.delay() #这就是将任务交给worker去执行了，这个任务在上面的时候已经加到队列中了，所以调用它的意思就是让worker去队列中找到send_sms这个任务去执行
#然后运行我们这个文件，右键运行就行，celery会在后台一直运行着




