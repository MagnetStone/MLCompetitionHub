import copy
from datetime import datetime, timedelta

from jinja2 import Environment, PackageLoader

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0800'
MAX_INTERVAL_DAY = 7


def generate(datas_):
    datas = copy.deepcopy(datas_)

    now_time = datetime.utcnow() + timedelta(hours=8)

    for data in datas:
        for c in data['competitions']:
            start_time = c['start_time']
            deadline = c['deadline']

            if start_time is not None:
                interval = now_time - start_time
                if interval.days < MAX_INTERVAL_DAY:
                    new_flag = True
                else:
                    new_flag = False
            else:
                new_flag = False

            # 转为标准时间格式字符串
            if start_time is None:
                start_time = '未给出具体时间'
            else:
                start_time = start_time.strftime(STANDARD_TIME_FORMAT)

            if deadline is None:
                deadline = '未给出具体时间'
            else:
                deadline = deadline.strftime(STANDARD_TIME_FORMAT)

            c['start_time'] = start_time
            c['deadline'] = deadline
            c['new_flag'] = new_flag

    env = Environment(loader=PackageLoader('actions'))

    update = now_time.strftime('%Y-%m-%dT%H:%M:%S+0800')

    # 生成 README.md
    template = env.get_template('main.j2')
    content = template.render(datas=datas, update=update)

    with open('README.md', 'w') as f:
        f.write(content)
