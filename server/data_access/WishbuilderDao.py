import sqlite3
import json
from datetime import datetime, timedelta
import markdown
import os

class Report:
    def __init__(self, report_json: str=None):
        if not report_json:
            # Valid File Test
            self.valid_files = False
            self.valid_files_report = ''

            # Directory Test
            self.pass_directory_test = False
            self.directory_test_report = ''

            # Configuration File Text
            self.pass_configuration_test = False
            self.configuration_test_report = ''

            # File Path Test
            self.pass_file_test = False
            self.file_test_report = ''

            # Run User Scripts
            self.pass_script_test = False
            self.script_test_report = ''

            # Key File Test
            self.pass_key_test = False
            self.key_test_report = ''

            # Example Data table
            self.data_preview = ''
            self.meta_data_preview = ''

            # Data Test Cases
            self.pass_data_tests = False
            self.data_tests_report = ''

            # Metadata Test Cases
            self.pass_meta_tests = False
            self.meta_tests_report = ''

            # Sample Comparison Test
            self.pass_sample_comparison = False
            self.sample_comparison_report = ''

            # Cleanup Test
            self.pass_cleanup = False
            self.cleanup_report = ''

            # Other (updates and strings of previous status report, if this is true, only the other_content will be
            # used when cast to a string
            self.other = False
            self.other_content = ''
        else:
            report_dict = json.loads(report_json)

            # Valid File Test
            self.valid_files = report_dict['valid_files']
            self.valid_files_report = report_dict['valid_files_report']

            # Directory Test
            self.pass_directory_test = report_dict['pass_directory_test']
            self.directory_test_report = report_dict['directory_test_report']

            # Configuration File Text
            self.pass_configuration_test = report_dict['pass_configuration_test']
            self.configuration_test_report = report_dict['configuration_test_report']

            # File Path Test
            self.pass_file_test = report_dict['pass_file_test']
            self.file_test_report = report_dict['file_test_report']

            # Run User Scripts
            self.pass_script_test = report_dict['pass_script_test']
            self.script_test_report = report_dict['script_test_report']

            # Key File Test
            self.pass_key_test = report_dict['pass_key_test']
            self.key_test_report = report_dict['key_test_report']

            # Example Data table
            self.data_preview = report_dict['data_preview']
            self.meta_data_preview = report_dict['meta_data_preview']

            # Data Test Cases
            self.pass_data_tests = report_dict['pass_data_tests']
            self.data_tests_report = report_dict['data_tests_report']

            # Metadata Test Cases
            self.pass_meta_tests = report_dict['pass_meta_tests']
            self.meta_tests_report = report_dict['meta_tests_report']

            # Sample Comparison Test
            self.pass_sample_comparison = report_dict['pass_sample_comparison']
            self.sample_comparison_report = report_dict['sample_comparison_report']

            # Cleanup Test
            self.pass_cleanup = report_dict['pass_cleanup']
            self.cleanup_report = report_dict['cleanup_report']

            # Other
            if 'other' in report_dict.keys():
                self.other = report_dict['other']
                self.other_content = report_dict['other_content']
            else:
                self.other = False
                self.other_content = ''

    def __str__(self) -> str:
        if self.other:
            return self.other_content
        else:
            out = self.valid_files_report
            out += self.directory_test_report
            out += self.configuration_test_report
            out += self.file_test_report
            out += self.script_test_report
            out += self.key_test_report
            out += self.meta_data_preview
            out += self.meta_tests_report
            out += self.data_preview
            out += self.data_tests_report
            out += self.sample_comparison_report
            out += self.cleanup_report
            return out

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class PullRequest:
    def __init__(self, pr: int, branch: str, date: str, e_date: float, feature_variables: int, meta_variables: int,
                 passed: bool, pr_id: int, num_samples: int, sha: str, time_elapsed: str, user: str, email: str,
                 status: str, report: str = None):
        self.pr = pr
        self.branch = branch
        self.date = date
        self.e_date = e_date
        self.feature_variables = feature_variables
        self.meta_variables = meta_variables
        self.passed = passed
        self.pr_id = pr_id
        self.num_samples = num_samples
        self.sha = sha
        self.time_elapsed = time_elapsed
        self.user = user
        self.email = email
        self.status = status
        self.report = Report(report)

    def __str__(self) -> str:
        out = "Pull Request Number: #{}\nBranch: {}\nDate: {}\neDate: {}\nNumber of Feature Variables: {}\n" \
              "Number of Metadata Variables: {}\nPassed: {}\nPull Request ID: {}\nNumber of Samples: {}\nSha: " \
              "{}\nTime Elapsed: {}\nUser: {}\nEmail: {}\nStatus: {}" \
            .format(self.pr, self.branch, self.date, self.e_date, self.feature_variables, self.meta_variables,
                    self.passed, self.pr_id, self.num_samples, self.sha, self.time_elapsed, self.user, self.email,
                    self.status)
        return out

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_updated(self):
        self.status = 'Updated'
        self.passed = True
        self.date = (datetime.now() - timedelta(hours=7)).strftime("%b %d, %y. %H:%m MST")

    def get_report_markdown(self) -> str:
        out = "<h1><center>{}</center></h1>\n".format(self.branch)
        out += '<h2><center> Status: {} </center></h2>\n<center>{}</center>\n\n'.format(self.status, self.date)
        out += str(self.report)
        out.replace('\t', ' ')
        return out

    def get_report_html(self) -> str:
        md = self.get_report_markdown()
        html = markdown.markdown(md)
        return html

    def check_if_passed(self) -> bool:
        passed = True
        if not self.report.valid_files:
            passed = False
        if not self.report.pass_directory_test:
            passed = False
        if not self.report.pass_configuration_test:
            passed = False
        if not self.report.pass_file_test:
            passed = False
        if not self.report.pass_script_test:
            passed = False
        if not self.report.pass_key_test:
            passed = False
        if not self.report.pass_data_tests:
            passed = False
        if not self.report.pass_meta_tests:
            passed = False
        if not self.report.pass_sample_comparison:
            passed = False
        if not self.report.pass_cleanup:
            passed = False
        self.passed = passed
        if passed:
            self.status = 'Complete'
            return True
        else:
            self.status = 'Failed'
            return False

class SqliteDao:
    def __init__(self, db_file):
        self.__file = db_file
        if not os.path.exists(db_file):
            self.create_db()
        self.__con = sqlite3.connect(db_file)
        self.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        self.__con.commit()
        self.__con.close()

    def open(self):
        self.__con = sqlite3.connect(self.__file)

    def create_db(self):
        self.open()
        c = self.__con.cursor()
        c.execute('drop table if exists PullRequests')
        c.execute("CREATE TABLE PullRequests(PR int not null, branch text, date text, eDate float, "
                  "featureVariables int, metaVariables int, passed boolean, prID int, numSamples int, "
                  "sha text not null PRIMARY KEY , timeElapsed text, user text, email text, status text, report text)")
        self.close()

    def insert_pr(self, pr: int, branch: str, date: str, e_date: float, feature_variables: int, meta_variables: int,
                  passed: bool, pr_id: int, num_samples: int, sha: str, time_elapsed: str, user: str, email: str,
                  status: str, report: str=None):
        self.open()
        c = self.__con.cursor()
        try:
            c.execute('insert into PullRequests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                      (pr, branch, date, e_date, feature_variables, meta_variables, passed, pr_id, num_samples, sha,
                       time_elapsed, user, email, status, report))
        except sqlite3.IntegrityError:
            print("Pull #{}, \'{}\' does not have a unique sha ({})".format(pr, branch, sha))
        self.close()

    def add_pr(self, pr: PullRequest):
        self.open()
        c = self.__con.cursor()
        c.execute('insert into PullRequests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (pr.pr, pr.branch, pr.date, pr.e_date, pr.feature_variables, pr.meta_variables, pr.passed, pr.pr_id,
                   pr.num_samples, pr.sha, pr.time_elapsed, pr.user, pr.email, pr.status, pr.report.to_json()))
        self.close()

    def get_prs(self, pr_number: int) -> [PullRequest]:
        try:
            self.open()
            c = self.__con.cursor()
            c.execute('select * from PullRequests where PR={}'.format(pr_number))
            data = c.fetchall()
            self.close()
            prs = []
            if data:
                for result in data:
                    pr = PullRequest(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                     result[7], result[8], result[9], result[10], result[11], result[12], result[13],
                                     result[14])
                    prs.append(pr)
            return prs
        except sqlite3.OperationalError:
            return None

    def get_reports(self, branch: str) -> [PullRequest]:
        try:
            self.open()
            c = self.__con.cursor()
            c.execute('select * from PullRequests where branch="{}"'.format(branch))
            data = c.fetchall()
            self.close()
            prs = []
            if data:
                for result in data:
                    pr = PullRequest(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                     result[7], result[8], result[9], result[10], result[11], result[12], result[13],
                                     result[14])
                    report = pr.get_report_html()
                    pr.report = report
                    prs.append(pr)
            return prs
        except sqlite3.OperationalError:
            return None

    def get_pr(self, pr_sha: str) -> PullRequest:
        try:
            self.open()
            c = self.__con.cursor()
            c.execute('select * from PullRequests where sha="{}"'.format(pr_sha))
            result = c.fetchone()
            self.close()
            if result:
                pr = PullRequest(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                 result[7], result[8], result[9], result[10], result[11], result[12], result[13],
                                 result[14])
            else:
                pr = None
            return pr
        except sqlite3.OperationalError:
            return None

    def get_prs_from_statement(self, sql_stmt: str) -> [PullRequest]:
        self.open()
        c = self.__con.cursor()
        c.execute(sql_stmt)
        data = c.fetchall()
        self.close()
        prs = []
        if data:
            for result in data:
                pr = PullRequest(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                 result[7], result[8], result[9], result[10], result[11], result[12], result[13],
                                 result[14])
                prs.append(pr)
        return prs

    def import_json(self, file: str, recreate=False):
        import uuid
        if recreate:
            self.create_db()
        with open(file) as fp:
            pr_history = json.load(fp)
            for pull in pr_history.keys():
                branch = pr_history[pull]['branch']
                date = pr_history[pull]['date']
                e_date = pr_history[pull]['eDate']
                feature_variables = pr_history[pull]['featureVariables']
                meta_variables = pr_history[pull]['metaVariables']
                passed = pr_history[pull]['passed']
                pr_id = pr_history[pull]['prID']
                pr = pr_history[pull]['prNum']
                num_samples = pr_history[pull]['samples']
                sha = pr_history[pull]['sha']
                time_elapsed = pr_history[pull]['timeElapsed']
                user = pr_history[pull]['user']

                if time_elapsed == 'update' or time_elapsed == 'updated':
                    status = 'update'
                    time_elapsed = 'N/A'
                elif time_elapsed == 'In Progress' or time_elapsed == 'Failed':
                    status = time_elapsed
                    time_elapsed = 'N/A'
                else:
                    if passed:
                        status = 'Passed'
                    else:
                        status = 'Failed'

                if user == 'glenrs':
                    email = 'grexsumsion@gmail.com'
                elif user == 'btc36':
                    email = 'benjamincookson94@gmail.com'
                elif user == 'kimballh':
                    email = 'hillkimball@gmail.com'
                else:
                    email = None

                if sha == 'null':
                    sha = str(uuid.uuid4())

                self.insert_pr(pr, branch, date, e_date, feature_variables, meta_variables, passed, pr_id, num_samples,
                               sha, time_elapsed, user, email, status)

    def get_all(self, return_objects=False):
        self.open()
        c = self.__con.cursor()
        if not return_objects:
            c.execute('select PR, sha from PullRequests')
        else:
            c.execute('select * from PullRequests')
        data = c.fetchall()
        self.close()
        if data:
            if not return_objects:
                prs = {}
                for i in range(len(data)):
                    prs.setdefault(data[i][0], []).append(data[i][1])
            else:
                prs = []
                for result in data:
                    pr = PullRequest(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                     result[7], result[8], result[9], result[10], result[11], result[12], result[13],
                                     result[14])
                    prs.append(pr)
        else:
            prs = None
        return prs

    def in_progress(self, pr: PullRequest) -> bool:
        self.open()
        c = self.__con.cursor()
        c.execute('select status from PullRequests where sha=\"{}\"'.format(pr.sha))
        data = c.fetchone()
        self.close()
        if data:
            if 'progress' in data[0] or 'Progress' in data[0]:
                return True
        return False

    def update(self, pr: PullRequest):
        self.open()
        c = self.__con.cursor()
        c.execute('delete from PullRequests where sha=\"{}\"'.format(pr.sha))
        self.close()
        self.add_pr(pr)

    def remove_pr(self, pr_number):
        self.open()
        c = self.__con.cursor()
        c.execute('delete from PullRequests where PR={}'.format(pr_number))