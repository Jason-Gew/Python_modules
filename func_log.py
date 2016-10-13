#!/usr/bin/env python
#	func_log.py is for testing basic log record functions
#	produced by Jason/Ge Wu
#
import logging
import os	# If log file path is certain, no need to import os library

# Must make sure the log file path in valid and available for R/W
path = 'test.log' 


def basic_log(level, message):
	'''
	%(module)s : invoked module
	%(funcName)s : invoked function
	%(lineno)d : invoked function line number
	%(thread)d : thread ID (May not have)
	%(threadName)s : thread name (May not have)
	%(process)d : process ID (May not have)
	'''
	logging.basicConfig(level = logging.DEBUG,  
						format = '[%(asctime)s %(filename)s] %(levelname)s: %(message)s',  
						datefmt = '%Y-%m-%d %H:%M:%S',  
						filename = path,  
						filemode ='a' # 'a' = append, 'w' = overwrite
						)  
	if level == 'debug':
		logging.debug(message)
	elif level == 'info':
		logging.info(message)
	elif level == 'warning':
		logging.warning(message)
	elif level ==  'error':
		logging.error('*** ' + message +  ' ***')
	elif level == 'critical':
		logging.critical('*** ' + message +  ' ***')
	else:
		logging.info('Unidentify:'+message)


def advanced_log(level, message, name=''):
	if os.path.exists(path):
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)
		log_file = logging.FileHandler(path)
		log_terminal = logging.StreamHandler()	# Output log information to terminal
		format = logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s')
	#	filter = logging.Filter(name.child)	# Set restrictions 
		log_file.setFormatter(format)
		log_terminal.setFormatter(format)
		logger.addHandler(log_file)
		logger.addHandler(log_terminal)
	#
		if level == 'debug':
			logger.debug(message)
		elif level == 'info':
			logger.info(message)
		elif level == 'warning':
			logger.warning(message)
		elif level ==  'error':
			logger.error('*** ' + message +  ' ***')
		elif level == 'critical':
			logger.critical('*** ' + message +  ' ***')
		else:
			logger.info('Unidentify:'+message)

		return True

	else:
		print ("\n*** Log file does not exists ***\n")
		return False

if __name__ == '__main__':
#	basic_log('error', 'Check it out!')
	advanced_log('critical', "issue 3", 'test_module')