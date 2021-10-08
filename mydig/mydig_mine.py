import datetime
import dns.message
import dns.query


def getResult(addr):
    answer = []
    rootservers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13',
                       '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53',
                       '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42',
                       '202.12.27.33']

    request = dns.message.make_query(addr, dns.rdatatype.A, dns.rdataclass.IN)

    for servers in rootservers:
        response = dns.query.udp(request, servers)
        if response.answer.__len__() != 0:
            if response.answer[0].__contains__(" A "):
                for n in response.answer:
                    answer.append(n)
            elif response.answer[0].__contains__(" CNAME "):
                return getResult(response.answer[0])

        for n in response.additional:
            ip = str(n).split()[4]
            if ip.__contains__('.'):
                rootservers.append(ip)
                del rootservers[0:len(rootservers) - 3]
    return answer


def saveToFile(text):
    f = open("mydig_mine_output.txt", 'w')
    f.write(text)
    f.close()


if __name__ == "__main__":
    file_text = ""
    addr = input('Please enter website : ')
    total_ttl = 0
    time1 = datetime.datetime.now()

    answer = getResult(addr)

    if len(answer) == 1 and 'CNAME' in answer.__str__():
        answer_temp = answer[0].__str__()
        answer_temp = answer_temp.split(" ")
        total_ttl += answer[0].ttl
        answer = getResult(answer_temp[4][0:-1])

    print('QUESTION SECTION: ')
    file_text += 'QUESTION SECTION: \n'
    print(addr, ' IN ', 'A')
    file_text += addr + ' IN A\n'

    print('\nANSWER SECTION: ')
    file_text += '\nANSWER SECTION: \n'
    for ans in answer:
        split_answer = ans.__str__().split(" ")
        result_ans = dns.rrset.from_text(addr, total_ttl + ans.ttl, dns.rdataclass.IN, dns.rdatatype.A,
                                         split_answer[-1])
        print(result_ans)
        file_text += result_ans.__str__() + "\n"

    time2 = datetime.datetime.now()
    t_result = time2 - time1
    print('\nQuery Time: ', t_result.microseconds / 1000, ' msec')
    file_text += '\nQuery Time: ' + str(t_result.microseconds / 1000) + ' msec'
    print('WHEN: ', datetime.datetime.now())
    file_text += '\nWHEN: ' + str(datetime.datetime.now())

    saveToFile(file_text)
