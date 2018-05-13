from django.core.paginator import Paginator
class CustomPaginator(Paginator):
    def __init__(self, current_page, range_num, *args, **kwargs):
        self.current_page = int(current_page)
        self.rang_num = range_num
        super().__init__(*args, **kwargs)

    def page_num_range(self):
        if self.num_pages <= self.rang_num:
            return range(1, self.num_pages + 1)
        part = int(self.rang_num / 2)
        if self.current_page <= part:
            start = 1
            end = self.rang_num + 1
            return range(start, end)
        if self.current_page + part > self.num_pages:
            start = self.num_pages - self.rang_num +1
            # start = self.current_page - part这是错误的
            end = self.num_pages + 1
            return range(start, end)
        else:
            start = self.current_page - part
            end = self.current_page + part + 1
            return range(start, end)