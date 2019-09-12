import unittest
import os
import yaml
# from Helper.HTMLTestRunner import HTMLTestRunner
from Helper.HTMLTestRunner_Chart import  HTMLTestRunner
import importlib
from Helper.EmailSender import EmailSender
import sys, getopt
import time

eutDir = os.path.dirname(__file__)
global_conf_file = os.path.join(eutDir, "Conf", "running.yaml")

with open(global_conf_file, "r") as f:
    global_conf = yaml.load(f)
runningProject = global_conf["project"]
casesDir = os.path.join(eutDir, "Projects", runningProject, "Cases")
logPath = os.path.join(eutDir, "Log", "log.txt")
# reportPath = os.path.join(eutDir, "Report", "report.html")
reportPath = os.path.join(eutDir, "Report", time.strftime("%Y-%m-%d %H:%M:%S")+"_Report.html")
project_config_path = os.path.join(eutDir, "Projects", runningProject, "%s.yaml" % runningProject)
with open(project_config_path, "r") as f:
    project_config = yaml.load(f)

pagesToRun = project_config["pagesToRun"]
modules = []
for fileName in os.listdir(casesDir):
    if fileName.startswith("Test") and fileName.endswith(".py"):
        moduleName = fileName[:-3]
        modules.append(moduleName)


class Test:

    # 收集测试用例
    def suite(self):
        su = unittest.TestSuite()
        if modules:
            for i in modules:
                m = "Projects.%s.Cases.%s" % (runningProject, i)
                s = importlib.import_module(m)
                clss = getattr(s, i)
                class_name = clss.__name__
                if pagesToRun:
                    for j in pagesToRun.split(", "):
                        if j == class_name:
                            for c in dir(clss):
                                if c.startswith("test_"):
                                    su.addTest(clss(c))
                else:
                    for c in dir(clss):
                        if c.startswith("test_"):
                            su.addTest(clss(c))
        return su

    def del_report(self):
        pass


if __name__ == '__main__':
    MyTests = Test()
    # html_file = os.path.join(eutDir, "Report", "report.html")
    html_file = reportPath
    log_file = os.path.join(eutDir, "Report", "execute.txt")
    Flag = False
    with open(reportPath, "wb") as f:
        # runner = HTMLTestRunner(stream=f, title='Automation Test Report', description='Project: %s' % runningProject)
        runner = HTMLTestRunner(
            title="Automation Test Report",
            description='Project: %s' % runningProject,
            stream=f,
            verbosity=2,
            retry=0,
            save_last_try=False)
        runner.run(MyTests.suite())

    size = os.path.getsize(html_file)

    # HTMLTestRunner_Chart报告,判断是否成功率
    if size == 0:
        Flag = True
    else:
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.readlines()
        Flag = True
        for i in html:
            if "概要{ 100.00% }" in i:
                Flag = False
                break

    if Flag:
        EmailSender.send_report(global_conf, reportPath)

    with open(log_file, 'a+') as f:
        f.write("执行时间:{now_time}    是否发送邮件:{Flag}    文件大小:{size}\n".format(now_time=time.strftime("%Y-%m-%d %H:%M:%S"), Flag=Flag,
                                                                           size=size))
