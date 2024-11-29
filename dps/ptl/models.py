from django.db import models


# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='仓库名称')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='仓库编码')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='仓库地址')
    company = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '仓库信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Location(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='所属仓库')
    label = models.ForeignKey('Label', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='标签')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='库位名称')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='库位编号')
    parent_location = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父级库位')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '库位信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Label(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name='标签类型',
                            choices=(('section', '灯塔'), ('node', '标签')))
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='标签外部编码')
    internal_id = models.IntegerField(blank=True, null=True, unique=True, verbose_name='标签内部ID')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '标签信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class StockInOrder(models.Model):
    """ 入库上架任务工单"""
    number = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name='入库单号')
    warehouse_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='仓库编号')
    warehouse_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='收货仓库')
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name='入库类型')
    src_order = models.CharField(max_length=50, blank=True, null=True, verbose_name='来源单号')
    is_complete = models.BooleanField(default=False, verbose_name='完成状态')
    is_void = models.BooleanField(default=False, verbose_name='是否作废')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    stock_staff = models.CharField(max_length=50, blank=True, null=True, verbose_name='入库人员')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '入库任务工单'
        verbose_name_plural = verbose_name

    @classmethod
    def get_number(cls):
        """ 生成入库单号"""
        from datetime import datetime
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        number = 'RK' +year + month + day + str(cls.objects.count() + 1).zfill(4)
        return number

    def __str__(self):
        return self.number


class StockInGoods(models.Model):
    """ 入库货物"""
    stock_in_order = models.ForeignKey(StockInOrder, on_delete=models.CASCADE, verbose_name='入库单号')
    goods_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='货物编码')
    goods_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='货物描述')
    plan_qty = models.IntegerField(blank=True, null=True, verbose_name='计划数量')
    actual_qty = models.IntegerField(blank=True, null=True, verbose_name='实际数量')
    is_complete = models.BooleanField(default=False, verbose_name='入库完成状态')
    batch = models.CharField(max_length=50, blank=True, null=True, verbose_name='批次号')
    supplier_batch = models.CharField(max_length=50, blank=True, null=True, verbose_name='厂商批次')
    location_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='库位编号')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '入库货品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_code


class StockOutOrder(models.Model):
    """ 出货下架任务工单"""
    number = models.CharField(max_length=32, blank=True, null=True, verbose_name='出库单号')
    warehouse_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='仓库编号')
    warehouse_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='出货仓库')
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name='出库类型')
    src_order = models.CharField(max_length=50, blank=True, null=True, verbose_name='来源单号')
    is_complete = models.BooleanField(default=False, verbose_name='完成状态')
    is_void = models.BooleanField(default=False, verbose_name='是否作废')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    stock_staff = models.CharField(max_length=50, blank=True, null=True, verbose_name='出库人员')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '出库任务工单'
        verbose_name_plural = verbose_name

    @classmethod
    def get_number(cls):
        """ 生成入库单号"""
        from datetime import datetime
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        number = 'CK' + year + month + day + str(cls.objects.count() + 1).zfill(4)
        return number

    def __str__(self):
        return self.number


class StockOutGoods(models.Model):
    """ 出库货物"""
    stock_out_order = models.ForeignKey(StockOutOrder, on_delete=models.CASCADE, verbose_name='出库单号')
    goods_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='货物编码')
    goods_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='货物描述')
    plan_qty = models.IntegerField(blank=True, null=True, verbose_name='货物数量')
    actual_qty = models.IntegerField(blank=True, null=True, verbose_name='实际数量')
    is_complete = models.BooleanField(default=False, verbose_name='出货完成状态')
    batch = models.CharField(max_length=50, blank=True, null=True, verbose_name='批次号')
    supplier_batch = models.CharField(max_length=50, blank=True, null=True, verbose_name='厂商批次')
    location_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='库位编号')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '出货货品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_code
