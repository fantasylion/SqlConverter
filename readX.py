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
mapJson = {}
mapJson2 = {}
values = []
maps = []
for bean in beanlist:
	
	beanName2 = bean.getAttribute('id')
	
	for beanName in beanNameList:

		if beanName2 == beanName:
			propertys = bean.getElementsByTagName('property')
			
			proJson = {}
			for pro in propertys:
				if pro.getAttribute('name') == 'jobDetail':
					objbean = pro.getElementsByTagName('bean')
					objectRef = objbean[0].getAttribute('p:targetObject-ref')
					targetMethod = objbean[0].getAttribute('p:targetMethod')
					proJson['targetObject']=objectRef
					proJson['targetMethod']=targetMethod
					print( objectRef + " : " + targetMethod )

				if pro.getAttribute('name') == 'cronExpression':
					value = pro.getAttribute('value')
					value = value.replace("#{p_schedule['", "")
					value = value.replace("']}", "")
					mapJson[beanName] = value
					proJson['timeExpreKey'] = value
			maps.append(proJson);
			mapJson2[beanName] = [objectRef, targetMethod, value]

print('-------------------------------')
fileName = 'schedule-pro.properties'
p = Properties(fileName)
properties = p.getProperties()

for pro in maps:
	pro['timeExpre'] = properties.get(pro['timeExpreKey'])
			
resultMap = {}

for key in mapJson:
	resultMap[key] = [mapJson.get(key), properties.get(mapJson.get(key))]

print(maps)


