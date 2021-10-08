import datetime, time
import dns.message, dns.query

# NAME : Kangmin Kim SBU ID: 111329652 COURSE : CSE310

# Since we don't have the proper output in the server, we need to look further
# 1. You can use a C name and restart it on the root server.
# 2. We can get the IP address from the additional section and use it as the next server.
# 3. If there is nothing in the additional section, the IP address cannot be obtained.
# address starts on the root server. So we will start looking for A record.
# (IP address search).

def get_answer_with_dns_by_recursive(name: str, ip: str, root: str):
    query = dns.message.make_query(name, dns.rdatatype.A, dns.rdataclass.IN)
    resp = dns.query.udp(query, ip)

    if resp.answer.__len__() != 0:
        if resp.answer[0].to_text().__contains__(" A "):
            return resp.answer

        elif resp.answer[0].to_text().__contains__(" CNAME "):
            for answer in resp.answer:
                file.write(answer.to_text() + "\n")
            return get_answer_with_dns_by_recursive(get_result(resp.answer[0].to_text()), root, root)

    if resp.additional.__len__() != 0:
        for addition in resp.additional:
            if " A " in addition.to_text():
                return get_answer_with_dns_by_recursive(name, get_result(addition.to_text()), root)
            else:
                continue

    else:
        for auth in resp.authority:
            if " NS " in auth.to_text():
                next_ip = get_answer_with_dns_by_recursive(get_result(auth.to_text()), root, root)
                return get_answer_with_dns_by_recursive(name, get_result(next_ip[0].to_text()), root)


def get_result(string: str):
    idx = len(string) - string[::-1].find(" ")
    return string[idx:]


output_name = 'mydig_output.txt'

url = input('Please enter url : ')
file = open(output_name, "w")

# Information of root servers is taken from "https://www.iana.org/domains/root/servers"

roots = ["198.41.0.4", "199.9.14.201", "192.33.4.12", "199.7.91.13", "192.203.230.10", "192.5.5.241", "192.112.36.4",
         "198.97.190.53", "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42", "202.12.27.33"]

file.write("QUESTION SECTION:\n" + url + " IN A\n\nANSWER SECTION:\n")

start_time = time.time()

answers = get_answer_with_dns_by_recursive(url, roots[len(roots)-1], roots[len(roots)-1])

end_time = time.time()
millis = str(int(round((end_time - start_time) * 1000)))
now = datetime.datetime.now().replace(microsecond=0)

for a in answers:
    file.write(a.to_text() + "\n")
file.write("\nQuery time: " + millis + " msec\nWHEN:  " + str(now))
