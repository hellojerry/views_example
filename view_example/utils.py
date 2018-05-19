from jira import JIRA


#conn = JIRA('https://petcoalm.atlassian.net',auth=('username','password'))
#
#def add_user():
#    user_to_create = input('Enter Username to Create: (ex: firstname.lastname\n')
#    user_email = input('Enter new User\'s Email Address:\n')
#    user_name = input('Enter new User\'s Full Name:\n')
#    active = True
#    conn.add_user(user_to_create, user_email, fullname=user_name, active=active)
#
class JIRAConnectionMixin(object):

	def get_jira_connection(self):
	
		conn = JIRA('https://your_url_goes_here.atlassian.net',auth=('username','password'))
		return conn
