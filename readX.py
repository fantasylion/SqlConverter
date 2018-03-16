# -*- coding:utf-8 -*-

import xml.dom.minidom
from Util import Properties

# 打开xml文档
dom = xml.dom.minidom.parse('spring-schedule-task-pro.xml')

# 得到文档元素对象
root = dom.documentElement

#  获取标签的ref
beanlist = root.getElementsByTagName('bean')
beanNameList = []
for list in beanlist:
	if list.getAttribute('class') == 'org.springframework.scheduling.quartz.SchedulerFactoryBean':
		refs = list.getElementsByTagName('ref')
		for ref in refs:
			beanName = ref.getAttribute('bean')
			beanNameList.append(beanName)


beanName2 = ''
maps = []
for bean in beanlist:
	
	beanName2 = bean.getAttribute('id')
	
	for beanName in beanNameList:

		if beanName2 == beanName:
			propertys = bean.getElementsByTagName('property')
			
			proJson = {'codeName':beanName}
			for pro in propertys:
				if pro.getAttribute('name') == 'jobDetail':
					objbean = pro.getElementsByTagName('bean')
					objectRef = objbean[0].getAttribute('p:targetObject-ref')
					targetMethod = objbean[0].getAttribute('p:targetMethod')
					proJson['targetObject']=objectRef
					proJson['targetMethod']=targetMethod
					# print( objectRef + " : " + targetMethod )

				if pro.getAttribute('name') == 'cronExpression':
					value = pro.getAttribute('value')
					value = value.replace("#{p_schedule['", "")
					value = value.replace("']}", "")
					proJson['timeExpreKey'] = value
			maps.append(proJson);


print('--------------开始创建SQL-----------------')
fileName = 'schedule-pro.properties'
p = Properties(fileName)
properties = p.getProperties()

for pro in maps:
	pro['timeExpre'] = properties.get(pro['timeExpreKey'])

# 打开文件
fo = open("test.sql", "w", encoding="utf-8")

count = 1
for pro in maps:
	sqlContext = "INSERT INTO t_sys_scheduler_task (id, bean_name, code, description, lifecycle, method_name, time_exp, version) VALUES (" + str(count) + ", '" + pro['targetObject'] + "', '" + pro['codeName'] + "', '暂无', 1, '" + pro['targetMethod'] + "', '" + pro['timeExpre'] + "', now());\n"
	fo.write( sqlContext )
	count = count + 1

# 关闭文件
fo.close()
print('--------------创建SQL结束-----------------')
# print(maps)


