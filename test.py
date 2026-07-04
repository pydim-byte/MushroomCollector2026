width = 800
s_width = 200

pages = 800 // 200
currenr_page = 0
# i want 0, 200, 400, 600 | 0, 200, 400, 600

for _ in range(6):
    print(currenr_page * s_width)
    currenr_page +=1
    print(currenr_page%pages, currenr_page%pages-1, currenr_page%(pages-1))
    currenr_page %= pages-1


