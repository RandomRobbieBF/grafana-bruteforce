# grafana-bruteforce



A tool that takes a combo username and password list and will attempt to bruteforce grafana login page.

Grafana will lock you out after 5 attempts so you need to ensure your proxy has multiple external ip's.

How to Run
---

Use supplied combo list

```
python3 grafana-brute.py -u http://localhost:3000
```


Use your own combo list.

```
python3 grafana-brute.py -u http://localhost:3000 -f mycombo.txt
```
