from webmonitor.package import package_bp
from webmonitor import models
from webmonitor.models import PackagePeriodType, PackagePaymentStatus
from flask import render_template, request, current_app, redirect, url_for
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.send_email import send_email
from webmonitor.utils.auth import login_required, admin_required
from webmonitor.utils.page import paginate
from datetime import datetime, timedelta
import stripe


# 用户或管理员获取所有的套餐模板（分页）
@package_bp.route('/package/template', methods=['GET'])
@login_required
def get_package_template_list(user):
    current_app.logger.info(f"user or admin get package template list user_id={user.id}")

    if user.role == 1:
        ret = paginate(models.PackageTemplate.query.filter_by(is_deleted=0))
        ret.items = [{
            "id": template.id,       
            "name": template.name,
            "period_count": template.period_count,
            "period_type": template.period_type,
            "period_check_count": template.period_check_count,
            "price": template.price,
            "update_time": template.update_time,
            "create_time": template.create_time,
            "hide": template.hide,
            "initial": template.initial,
        } for template in ret.items]

    else:
        ret = paginate(models.PackageTemplate.query.filter_by(is_deleted=0, hide=0))
        ret.items = [{
            "id": template.id,       
            "name": template.name,
            "period_count": template.period_count,
            "period_type": template.period_type,
            "period_check_count": template.period_check_count,
            "price": template.price,
            "update_time": template.update_time,
            "create_time": template.create_time,
        } for template in ret.items]

    return ok(data=ret)
    


# 管理员创建套餐模板
@package_bp.route('/package/template', methods=['POST'])
@admin_required
def create_package_template(user):
    name = request.form.get('name')
    period_count        = request.form.get('period_count')
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    hide                = request.form.get('hide')
    initial             = request.form.get('initial')
    
    current_app.logger.info(f"admin create package template user_id={user.id} name={name} period_count={period_count} period_type={period_type} period_check_count={period_check_count} price={price} hide={hide} initial={initial}")

    if not all([name, period_count, period_type, period_check_count, price, hide, initial]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    period_count        = int(period_count)
    period_type         = int(period_type)
    period_check_count  = int(period_check_count)
    price               = int(price)
    hide                = int(hide) 
    initial             = int(initial) 
    if period_count < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_type not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, PackagePeriodType.PERMANENT.id]:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_check_count < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if price < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if hide not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    if initial not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    
    template = models.PackageTemplate(
        name=name,
        period_count=period_count,
        period_type=period_type,
        period_check_count=period_check_count,
        price=price,
        hide=hide,
        initial=initial,
    )
    
    models.db.session.add(template)
    models.db.session.commit()
    return ok()


# 管理员修改套餐模板
@package_bp.route('/package/template/<int:template_id>', methods=['PUT'])
@admin_required
def modify_package_template(user, template_id):
    name = request.form.get('name')
    period_count        = request.form.get('period_count')
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    hide                = request.form.get('hide')
    initial             = request.form.get('initial')
    
    current_app.logger.info(f"admin modify package template user_id={user.id} template_id={template_id} name={name} period_count={period_count} period_type={period_type} period_check_count={period_check_count} price={price} hide={hide} initial={initial}")

    if period_count and int(period_count) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_type and int(period_type) not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, PackagePeriodType.PERMANENT.id]:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_check_count and int(period_check_count) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if price and int(price) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if hide and int(hide) not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    if initial and int(initial) not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    
    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=0).first()
    if not template or template.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    if name: 
        template.name = name
    if period_count: 
        template.period_count = int(period_count)
    if period_type:
        template.period_type = int(period_type)
    if period_check_count:
        template.period_check_count = int(period_check_count)
    if price:
        template.price = int(price)
    if hide:
        template.hide = int(hide)
    if initial:
        template.initial = int(initial)
    
    models.db.session.commit()
    return ok()


# 管理员删除套餐模板（软删除）
@package_bp.route('/package/template/<int:template_id>', methods=['DELETE'])
@admin_required
def delete_package_template(user, template_id):
    current_app.logger.info(f"admin delete package template user_id={user.id} template_id={template_id}")

    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=0).first()
    if not template or template.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    template.is_deleted = 1
    models.db.session.commit()
    return ok()


# 管理员获取软删除的套餐模板（分页）
@package_bp.route('/package/template/deleted', methods=['GET'])
@admin_required
def get_deleted_package_template_list(user):
    current_app.logger.info(f"admin get deleted package template list user_id={user.id}")

    tempaltes = paginate(models.PackageTemplate.query.filter_by(is_deleted=1))
    return ok(data=[{
        "id": template.id,       
        "name": template.name,
        "period_count": template.period_count,
        "period_type": template.period_type,
        "period_check_count": template.period_check_count,
        "price": template.price,
        "update_time": template.update_time,
        "create_time": template.create_time,
    } for template in tempaltes])


# 管理员恢复软删除的套餐模板
@package_bp.route('/package/template/<int:template_id>/recover', methods=['PUT'])
@admin_required
def recover_package_template(user, template_id):
    current_app.logger.info(f"admin recover package template user_id={user.id} template_id={template_id}")

    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=1).first()
    if not template or template.is_deleted == 0:
        return abort(ErrorCode.NOT_FOUND)
    
    template.is_deleted = 0
    models.db.session.commit()
    return ok()




# 用户或管理员获取自己的所有套餐（分页）
@package_bp.route('/package', methods=['GET'])
@login_required 
def get_package_list(user):
    current_app.logger.info(f"user or admin get package list user_id={user.id}")

    ret = paginate(models.Package.query.filter_by(user_id=user.id, is_deleted=0))
    ret.items = [{
        "id": package.id,       
        "name": package.name,
        "period_count": package.period_count,
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "end_time": package.end_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "period_left": package.period_left,
        "check_count_left": package.check_count_left,
        "update_time": package.update_time,
        "create_time": package.create_time,
    } for package in ret.items]
    return ok(data=ret)


# 管理员获取特定用户的所有套餐（分页）
@package_bp.route('/user/<int:user_id>/package', methods=['GET'])
@admin_required
def get_user_package_list(user, user_id):
    current_app.logger.info(f"admin get user package list user_id={user.id} user_id={user_id}")

    ret = paginate(models.Package.query.filter_by(user_id=user_id, is_deleted=0))
    ret.items = [{
        "id": package.id,       
        "name": package.name,
        "period_count": package.period_count,
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "end_time": package.end_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "period_left": package.period_left,
        "check_count_left": package.check_count_left,
        "update_time": package.update_time,
        "create_time": package.create_time,
    } for package in ret.items]
    return ok(data=ret)


# 管理员删除套餐（软删除）
@package_bp.route('/package/<int:package_id>', methods=['DELETE'])
@admin_required
def admin_delete_package(user, package_id):
    current_app.logger.info(f"admin delete package user_id={user.id} package_id={package_id}")

    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    package.is_deleted = 1
    package.user.check_quota()
    models.db.session.commit()
    return ok()


# 管理员获取特定用户软删除的套餐（分页）
@package_bp.route('/package/user/<int:user_id>/deleted', methods=['GET'])
@admin_required
def get_deleted_user_package_list(user, user_id):
    current_app.logger.info(f"admin get deleted user package list user_id={user.id} user_id={user_id}")

    packages = paginate(models.Package.query.filter_by(user_id=user_id, is_deleted=1))
    return ok(data=[{
        "id": package.id,       
        "name": package.name,
        "period_count": package.period_count,
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "end_time": package.end_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "period_left": package.period_left,
        "check_count_left": package.check_count_left,
        "update_time": package.update_time,
        "create_time": package.create_time,
    } for package in packages])


# 管理员恢复软删除的套餐
@package_bp.route('/package/<int:package_id>/recover', methods=['PUT'])
@admin_required
def recover_package(user, package_id):
    current_app.logger.info(f"admin recover package user_id={user.id} package_id={package_id}")

    package = models.Package.query.filter_by(id=package_id, is_deleted=1).first()
    if not package or package.is_deleted == 0:
        return abort(ErrorCode.NOT_FOUND)
    
    package.is_deleted = 0
    package.user.check_quota()
    models.db.session.commit()
    return ok()


# 管理员修改套餐
@package_bp.route('/package/<int:package_id>', methods=['PUT'])
@admin_required
def admin_modify_package(user, package_id):
    name = request.form.get('name')
    period_count        = request.form.get('period_count')
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    period_left         = request.form.get('period_left')
    check_count_left    = request.form.get('check_count_left')
    
    current_app.logger.info(f"admin modify package user_id={user.id} package_id={package_id} name={name} period_count={period_count} period_type={period_type} period_check_count={period_check_count} price={price}")

    if period_count and int(period_count) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_type and int(period_type) not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, PackagePeriodType.PERMANENT.id]:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_check_count and int(period_check_count) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if price and int(price) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_left and int(period_left) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if check_count_left and int(check_count_left) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    
    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    if name: 
        package.name = name
    if period_count: 
        package.period_count = int(period_count)
    if period_type:
        package.period_type = int(period_type)
    if period_check_count:
        package.period_check_count = int(period_check_count)
    if price:
        package.price = int(price)
    if period_left:
        package.period_left = int(period_left)
    if check_count_left:
        package.check_count_left = int(check_count_left)
    
    models.db.session.commit()

    package.user.check_quota()
    models.db.session.commit()
    return ok()


# 用户为自己购买某个模板的套餐
@package_bp.route('/package/purchase/<int:template_id>', methods=['POST'])
@login_required
def purchase_package(user, template_id):
    current_app.logger.info(f"user purchase package user_id={user.id} template_id={template_id}")

    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=0).first()
    if not template or template.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    # 创建session
    done_url = current_app.config['FRONTEND_BASE_URL'] + "/package/purchase/done?session_id={CHECKOUT_SESSION_ID}"
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": current_app.config['STRIPE_PRICE_ID'],
                "quantity": template.price
            }
        ],
        mode="payment",
        success_url=done_url,
        cancel_url=done_url,
    )
    current_app.logger.info(f"create stripe session_id={session['id']}")

    # 创建payment
    payment = models.PackagePayment(
        user_id     = user.id,
        template_id = template_id,
        session_id  = session["id"],
        status      = PackagePaymentStatus.PENDING.id,
    )
    models.db.session.add(payment)
    models.db.session.commit()

    return ok(data={ "session_id" : session["id"] })
    

# 用户套餐付款结束webhook
@package_bp.route('/package/purchase/webhook', methods=['POST'])
def purchase_package_webhook():
    # 获取event
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_ENDPOINT_KEY']
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e
    
    current_app.logger.info(f"webhook event type={event['type']}")

    # 如果不是支付成功
    if event['type'] != 'payment_intent.succeeded':
        abort(ErrorCode.PARAMS_INVALID, f'Unhandled webhook event type: {event['type']}')

    # 支付成功，获取session_id查询Payment对象
    payment_intent_id = event['data']['object']['id']
    session = stripe.checkout.Session.list(payment_intent=payment_intent_id, limit=1)['data'][0]
    session_id = session['id']

    current_app.logger.info(f"payment success session_id={session_id}")

    payment = models.PackagePayment.query.filter_by(session_id=session_id).first()
    if not payment:
        return abort(ErrorCode.NOT_FOUND)

    user_id = payment.user_id
    user = models.User.query.filter_by(id=user_id, is_deleted=0).first()
    if not user or user.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)

    template_id = payment.template_id
    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=0).first()
    if not template or template.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    # 添加套餐
    package = models.Package(
        user_id                     = user_id,
        name                        = template.name,
        period_count                = template.period_count,
        period_type                 = template.period_type,
        period_check_count          = template.period_check_count,
        price                       = template.price,
    )
    package.init(datetime.now())
    package.update()

    # 更新payment状态
    payment.status = PackagePaymentStatus.PAID.id
    
    models.db.session.add(package)
    models.db.session.commit()

    user.check_quota()
    models.db.session.commit()

    return ok()


# 管理员为某个用户购买某个模板的套餐，创建套餐
@package_bp.route('/package/purchase/<int:template_id>/user/<int:user_id>', methods=['POST'])
@admin_required
def admin_add_package(admin, template_id, user_id):
    current_app.logger.info(f"admin purchase package user_id={admin.id} template_id={template_id} user_id={user_id}")

    user = models.User.query.filter_by(id=user_id, is_deleted=0).first()
    if not user or user.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)

    template = models.PackageTemplate.query.filter_by(id=template_id, is_deleted=0).first()
    if not template or template.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    # NO 扣费
    
    package = models.Package(
        user_id                     = user.id,
        name                        = template.name,
        period_count                = template.period_count,
        period_type                 = template.period_type,
        period_check_count          = template.period_check_count,
        price                       = template.price,
    )
    package.init(datetime.now())
    package.update()

    models.db.session.add(package)
    models.db.session.commit()

    user.check_quota()
    models.db.session.commit()

    return ok()
