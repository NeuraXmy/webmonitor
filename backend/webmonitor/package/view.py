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
from webmonitor.utils.apscheduler import scheduler
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
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    hide                = request.form.get('hide')
    initial             = request.form.get('initial')
    
    current_app.logger.info(f"admin create package template user_id={user.id} name={name} period_type={period_type} period_check_count={period_check_count} price={price} hide={hide} initial={initial}")

    if not all([name, period_type, period_check_count, price, hide, initial]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    period_type         = int(period_type)
    period_check_count  = int(period_check_count)
    price               = int(price)
    hide                = int(hide) 
    initial             = int(initial) 
    if period_type not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, 
                           PackagePeriodType.PERMANENT.id, PackagePeriodType.TEST.id]:
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
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    hide                = request.form.get('hide')
    initial             = request.form.get('initial')
    
    current_app.logger.info(f"admin modify package template user_id={user.id} template_id={template_id} name={name} period_type={period_type} period_check_count={period_check_count} price={price} hide={hide} initial={initial}")

    if period_type and int(period_type) not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, 
                                                PackagePeriodType.PERMANENT.id, PackagePeriodType.TEST.id]:
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
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "check_count_left": package.check_count_left,
        "cancel_at_next": package.cancel_at_next,
        "need_payment": package.need_payment,
        "is_last_payment_failed": package.is_last_payment_failed,
        "is_expired": package.is_expired(),
        "update_time": package.update_time,
        "create_time": package.create_time,
    } for package in ret.items]
    return ok(data=ret)


# 用户或管理员获取自己正在使用的套餐
@package_bp.route('/package/using', methods=['GET'])
@login_required
def get_using_package(user):
    current_app.logger.info(f"user or admin get using package user_id={user.id}")

    package = user.get_current_package()
    if not package:
        return ok()
    return ok(data={
        "id": package.id,
        "name": package.name,
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "check_count_left": package.check_count_left,
        "cancel_at_next": package.cancel_at_next,
        "need_payment": package.need_payment,
        "is_last_payment_failed": package.is_last_payment_failed,
        "is_expired": package.is_expired(),
        "update_time": package.update_time,
        "create_time": package.create_time,
    })


# 管理员获取特定用户的所有套餐（分页）
@package_bp.route('/user/<int:user_id>/package', methods=['GET'])
@admin_required
def get_user_package_list(user, user_id):
    current_app.logger.info(f"admin get user package list user_id={user.id} user_id={user_id}")

    ret = paginate(models.Package.query.filter_by(user_id=user_id, is_deleted=0))
    ret.items = [{
        "id": package.id,       
        "name": package.name,
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "check_count_left": package.check_count_left,
        "cancel_at_next": package.cancel_at_next,
        "need_payment": package.need_payment,
        "is_last_payment_failed": package.is_last_payment_failed,
        "is_expired": package.is_expired(),
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
        "period_type": package.period_type,
        "period_check_count": package.period_check_count,
        "price": package.price,
        "start_time": package.start_time,
        "current_period_start_time": package.current_period_start_time,
        "current_period_end_time": package.current_period_end_time,
        "check_count_left": package.check_count_left,
        "cancel_at_next": package.cancel_at_next,
        "need_payment": package.need_payment,
        "is_last_payment_failed": package.is_last_payment_failed,
        "is_expired": package.is_expired(),
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
    period_type         = request.form.get('period_type')
    period_check_count  = request.form.get('period_check_count')
    price               = request.form.get('price')
    check_count_left    = request.form.get('check_count_left')
    need_payment        = request.form.get('need_payment')
    cancel_at_next      = request.form.get('cancel_at_next')
    
    current_app.logger.info(f"admin modify package user_id={user.id} package_id={package_id} name={name} period_type={period_type} period_check_count={period_check_count} price={price}")

    if period_type and int(period_type) not in [PackagePeriodType.DAY.id, PackagePeriodType.MONTH.id, PackagePeriodType.YEAR.id, PackagePeriodType.PERMANENT.id]:
        return abort(ErrorCode.PARAMS_INVALID)
    if period_check_count and int(period_check_count) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if price and int(price) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if check_count_left and int(check_count_left) < 0:
        return abort(ErrorCode.PARAMS_INVALID)
    if need_payment and int(need_payment) not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    if cancel_at_next and int(cancel_at_next) not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID)
    
    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    # 没有付款方式的套餐不能设置为需要付款
    if need_payment and int(need_payment) == 1 and package.stripe_payment_method_id is None:
        return abort(ErrorCode.PARAMS_INVALID, "Need payment but no payment method for this package.")
    
    if name: 
        package.name = name
    if period_type:
        package.period_type = int(period_type)
    if period_check_count:
        package.period_check_count = int(period_check_count)
    if price:
        package.price = int(price)
    if check_count_left:
        package.check_count_left = int(check_count_left)
    if need_payment:
        package.need_payment = int(need_payment)
    if cancel_at_next:
        package.cancel_at_next = int(cancel_at_next)
    
    models.db.session.commit()

    package.user.check_quota()
    models.db.session.commit()
    return ok()


# 用户取消套餐（下个周期取消）
@package_bp.route('/package/<int:package_id>/cancel', methods=['POST'])
@login_required
def cancel_package(user, package_id):
    current_app.logger.info(f"user cancel package user_id={user.id} package_id={package_id}")

    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    package.cancel_at_next = 1
    models.db.session.commit()
    return ok()


# 用户恢复套餐（下个周期续订）
@package_bp.route('/package/<int:package_id>/resume', methods=['POST'])
@login_required
def resume_package(user, package_id):
    current_app.logger.info(f"user resume package user_id={user.id} package_id={package_id}")

    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    package.cancel_at_next = 0
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
    
    # 如果没有，为用户创建stripe customer
    if user.stripe_customer_id is None:
        customer = stripe.Customer.create(
            name=f'{user.id}@webmonitor', 
            email=user.email
        )
        user.stripe_customer_id = customer['id']
        models.db.session.commit()
        current_app.logger.info(f"create stripe customer_id={customer['id']} for user_id={user.id}")

    # 创建付款session
    success_url = current_app.config['FRONTEND_BASE_URL'] + "/package/purchase/success?session_id={CHECKOUT_SESSION_ID}"
    cancel_url  = current_app.config['FRONTEND_BASE_URL'] + "/package/purchase/error?session_id={CHECKOUT_SESSION_ID}"
    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=["card"],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{
            'price_data': {
                'currency': 'cny',
                'product_data': {
                    'name': template.name,
                }, 
                'unit_amount': template.price,  
            },
            'quantity': 1,
        }],
        payment_intent_data={
            'setup_future_usage': 'off_session',
            'metadata': {
                'url': current_app.config['FRONTEND_BASE_URL'],
                'type': 'package_first_purchase',  
                'user_id': user.id,
                'template_name': template.name,
                'template_period_type': template.period_type,
                'template_period_check_count': template.period_check_count,
                'template_price': template.price,
            },
        },
    )
    current_app.logger.info(f"create stripe session_id={session['id']}")

    return ok(data={ 
        "session_id" : session["id"],
        "url"        : session["url"],
    })
    

# 套餐 stripe webhook
@package_bp.route('/package/purchase/webhook', methods=['POST'])
def purchase_package_webhook():
    # 获取event和安全检查
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
    current_app.logger.info(f"stripe webhook get event type={event['type']}")

    # 支付成功事件
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_intent_id = payment_intent['id']
        metadata = payment_intent['metadata']

        # 不是本域名的事件不处理
        if 'url' not in metadata or metadata['url'] != current_app.config['FRONTEND_BASE_URL']:
            return ok() 

        current_app.logger.info(f"payment_intent.succeeded for payment_intent_id={payment_intent_id} metadata={metadata}")

        # 套餐首次购买
        if metadata['type'] == 'package_first_purchase':
            current_app.logger.info(f"package first purchase for user_id={metadata['user_id']} template_name={metadata['template_name']}")

            user_id = int(metadata['user_id'])
            template_name = metadata['template_name']
            template_period_type = int(metadata['template_period_type'])
            template_period_check_count = int(metadata['template_period_check_count'])
            template_price = int(metadata['template_price'])

            user = models.User.query.filter_by(id=user_id, is_deleted=0).first()
            if not user or user.is_deleted == 1:
                return abort(ErrorCode.NOT_FOUND)
            
            # 保存付款方式到用户
            payment_method_id = payment_intent['payment_method']
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=user.stripe_customer_id,
            )
            current_app.logger.info(f"attach payment_method_id={payment_method_id} to user_id={user.id}")

            # 创建套餐
            package = models.Package(
                user_id                     = user.id,
                name                        = template_name,
                period_type                 = template_period_type,
                period_check_count          = template_period_check_count,
                price                       = template_price,
                start_time                  = datetime.now(),
                current_period_start_time   = datetime.now(),
                current_period_end_time     = PackagePeriodType.get_next_time(template_period_type, datetime.now()),
                check_count_left            = template_period_check_count,
                cancel_at_next              = 0,
                need_payment                = 1,
                is_last_payment_failed      = 0,
                stripe_payment_method_id    = payment_method_id,
            )
            models.db.session.add(package)
            models.db.session.commit()
            current_app.logger.info(f"create package_id={package.id} for user_id={user.id}")

            user.check_quota()

            # 创建支付成功记录
            payment = models.PackagePayment(
                stripe_payment_intent_id = payment_intent_id,
                name = f'{template_name} 首次购买',
                status = PackagePaymentStatus.SUCCEEDED.id,
                msg = '',
                pay_time = datetime.now(),
                amount = template_price,
                package_id = package.id,
            )
            models.db.session.add(payment)
            models.db.session.commit()
            current_app.logger.info(f"create payment_id={payment.id} for package_id={package.id}")
    
    # 未处理的事件
    else:
        abort(ErrorCode.PARAMS_INVALID, f"Unhandled webhook event type: {event['type']}")
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
    
    package = models.Package(
        user_id                     = user.id,
        name                        = template.name,
        period_type                 = template.period_type,
        period_check_count          = template.period_check_count,
        price                       = template.price,
        start_time                  = datetime.now(),
        current_period_start_time   = datetime.now(),
        current_period_end_time     = PackagePeriodType.get_next_time(template.period_type, datetime.now()),
        check_count_left            = template.period_check_count,
        cancel_at_next              = 0,
        need_payment                = 0,
        is_last_payment_failed      = 0,
        stripe_payment_method_id    = None,
    )
    models.db.session.add(package)
    models.db.session.commit()

    user.check_quota()
    models.db.session.commit()

    return ok()



# 进行套餐的更新收款
def package_recurring_charge(package):
    current_app.logger.info(f"package recurring charge for package_id={package.id}")
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=package.price,
            currency='cny',
            payment_method=package.stripe_payment_method_id,
            customer=package.user.stripe_customer_id,
            confirm=True, 
            off_session=True,  
            metadata={
                'url': current_app.config['FRONTEND_BASE_URL'],
                'type': 'package_renewal',
                'package_id': package.id,
            }
        )
        return { "success": True, "payment_intent_id": payment_intent.id }
    except stripe.error.StripeError as e:
        return { "success": False, "error": e }


# 进行套餐的更新检查
def check_package_update(package):
    # 套餐需要更新
    while datetime.now() >= package.current_period_end_time:
        current_app.logger.info(f"package need update for package_id={package.id}, current_period_end_time={package.current_period_end_time}")

        # 套餐上次付款失败
        if package.is_last_payment_failed == 1:
            current_app.logger.info(f"package last payment failed for package_id={package.id}")
            # 不做处理，等待用户重新付款
            return

        # 套餐被用户取消
        if package.cancel_at_next == 1:
            # 直接删除
            package.is_deleted = 1
            models.db.session.commit()
            package.user.check_quota()
            models.db.session.commit()
            current_app.logger.info(f"package canceled for package_id={package.id}")
            return
        
        # 套餐需要付款
        if package.need_payment == 1:
            # 尝试收款
            result = package_recurring_charge(package)
            # 付款失败
            if not result['success']:
                current_app.logger.info(f"package recurring charge failed for package_id={package.id}")
                # 记录付款失败状态
                package.is_last_payment_failed = 1
                # 添加付款失败记录
                payment = models.PackagePayment(
                    stripe_payment_intent_id = None,
                    status = PackagePaymentStatus.FAILED.id,
                    name = f'{package.name} 续费',
                    msg = result['error'],
                    amount = package.price,
                    pay_time = datetime.now(),
                    package_id = package.id,
                )
                models.db.session.add(payment)
                models.db.session.commit()
                package.user.check_quota()
                models.db.session.commit()
                return
            
            # 套餐付款成功
            else:   
                current_app.logger.info(f"package recurring charge success for package_id={package.id}")
                # 添加付款成功记录
                package.is_last_payment_failed = 0
                payment = models.PackagePayment(
                    stripe_payment_intent_id = result['payment_intent_id'],
                    name = f'{package.name} 续费',
                    status = PackagePaymentStatus.SUCCEEDED.id,
                    msg = '',
                    amount = package.price,
                    pay_time = datetime.now(),
                    package_id = package.id,
                )
                models.db.session.add(payment)
                models.db.session.commit()

        # 更新套餐
        start = package.current_period_start_time
        if package.period_type == PackagePeriodType.TEST.id:
            start = datetime.now()
        package.current_period_start_time = start
        package.current_period_end_time = PackagePeriodType.get_next_time(package.period_type, start)
        package.check_count_left = package.period_check_count
        models.db.session.commit()

        package.user.check_quota()
        models.db.session.commit()

        current_app.logger.info(f"package update for package_id={package.id} success, current_period_end_time={package.current_period_end_time}")


# 套餐定期更新任务
@scheduler.task('cron', id='package_update', second=f'*/5')
def package_update_task():
    with scheduler.app.app_context():
        current_app.logger.info(f"package update task at {datetime.now()}")
        packages = models.Package.query.filter_by(is_deleted=0).all()
        for package in packages:
            try:
                check_package_update(package)
            except Exception as e:
                import traceback
                current_app.logger.error(f"check package update failed package_id={package.id} error={e}")
                current_app.logger.error(traceback.format_exc())
                continue



# 用户或管理员获取自己的套餐付款记录（分页）
@package_bp.route('/package/<int:package_id>/payment', methods=['GET'])
@login_required
def get_package_payment_list(user, package_id):
    current_app.logger.info(f"user or admin get package payment list user_id={user.id} package_id={package_id}")
    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    if package.user_id != user.id and user.role != 1:
        return abort(ErrorCode.FORBIDDEN)

    ret = paginate(models.PackagePayment.query.filter_by(package_id=package_id).order_by(models.PackagePayment.pay_time.desc()))
    ret.items = [{
        "id": payment.id,       
        "name": payment.name,
        "status": payment.status,
        "msg": payment.msg,
        "pay_time": payment.pay_time,
        "amount": payment.amount,
        "update_time": payment.update_time,
        "create_time": payment.create_time,
    } for payment in ret.items]
    return ok(data=ret)


# 修改特定套餐的支付方式
@package_bp.route('/package/<int:package_id>/payment_method', methods=['PUT'])
@login_required
def change_package_payment_method(user, package_id):
    payment_method = request.form.get('payment_method')
    current_app.logger.info(f"user change package payment method user_id={user.id} package_id={package_id} payment_method={payment_method}")

    package = models.Package.query.filter_by(id=package_id, is_deleted=0).first()
    if not package or package.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    if package.user_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 不需要付款的套餐不能修改支付方式
    if not package.need_payment:
        return abort(ErrorCode.PACKAGE_NOT_NEED_PAYMENT)
    
    # 取消的套餐不能修改支付方式
    if package.cancel_at_next:
        return abort(ErrorCode.PACKAGE_CANCELED)
    
    # 不应该出现这种情况
    if not user.stripe_customer_id:
        return abort(ErrorCode.NOT_FOUND, "User has no stripe customer id.")

    # 绑定
    current_app.logger.info(f"attach payment_method_id={payment_method} to customer_id={user.stripe_customer_id}")
    stripe.PaymentMethod.attach(
        payment_method,
        customer=user.stripe_customer_id,
    )

    # 更新套餐
    package.stripe_payment_method_id = payment_method
    models.db.session.commit()

    # 如果上次续费失败，立即尝试续费
    if package.is_last_payment_failed == 1:
        current_app.logger.info(f"retry package recurring charge for package_id={package.id}")
        result = package_recurring_charge(package)
        # 付款失败
        if not result['success']:
            current_app.logger.info(f"package recurring charge failed for package_id={package.id}")
            # 记录付款失败状态
            package.is_last_payment_failed = 1
            # 添加付款失败记录
            payment = models.PackagePayment(
                stripe_payment_intent_id = None,
                status = PackagePaymentStatus.FAILED.id,
                name = f'{package.name} 续费',
                msg = result['error'],
                amount = package.price,
                pay_time = datetime.now(),
                package_id = package.id,
            )
            models.db.session.add(payment)
            models.db.session.commit()
            package.user.check_quota()
            models.db.session.commit()
            
        # 套餐付款成功
        else:   
            current_app.logger.info(f"package recurring charge success for package_id={package.id}")
            # 添加付款成功记录
            package.is_last_payment_failed = 0
            payment = models.PackagePayment(
                stripe_payment_intent_id = result['payment_intent_id'],
                name = f'{package.name} 续费',
                status = PackagePaymentStatus.SUCCEEDED.id,
                msg = '',
                amount = package.price,
                pay_time = datetime.now(),
                package_id = package.id,
            )
            models.db.session.add(payment)
            models.db.session.commit()

            # 更新套餐（从当前时间开始）
            start = datetime.now()
            package.current_period_start_time = start
            package.current_period_end_time = PackagePeriodType.get_next_time(package.period_type, start)
            package.check_count_left = package.period_check_count
            models.db.session.commit()

            package.user.check_quota()
            models.db.session.commit()

    return ok()