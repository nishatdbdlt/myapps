# controllers/portal.py
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager

class PreSalesPortal(http.Controller):

    @http.route(['/my/pre_sales', '/my/pre_sales/page/<int:page>'], type='http', auth='user', website=True)
    def portal_pre_sales_list(self, page=1, **kw):
        PreSales = request.env['pre.sales'].sudo()

        #Filter only current logged-in user's records
        domain = [('user_id', '=', request.env.user.id)]
        
        
        #search filter
        amount_status = kw.get('amount_status')
        client_category = kw.get('client_category')
        profile_name = kw.get('profile_name')
        service_type = kw.get('service_type')

        if amount_status:
            domain.append(('amount_status', '=', amount_status))

        if client_category:
            domain.append(('client_category', '=', client_category))

        if profile_name:
            domain.append(('profile_name', '=', int(profile_name)))

        if service_type:
            domain.append(('service_type', '=', int(service_type)))
            
               

        url = '/my/pre_sales'
        total = PreSales.search_count(domain)
        
        # Calculate pagination manually
        page_count = 10  # items per page
        pager = portal_pager(
            url=url,
            total=total,
            page=page,
            step=page_count,
            url_args=kw
        )
        
        # Use the pager values
        offset = (page - 1) * page_count
        limit = page_count

        records = PreSales.search(domain, limit=limit, offset=offset, order='date desc')

        return request.render('pre_sales.pre_sales_portal_list', {
            'pre_sales_records': records,
            'pager': pager,
            'task_type': kw.get('task_type', False),
        })

    @http.route(['/my/pre_sales/<int:record_id>'], type='http', auth='user', website=True)
    def portal_pre_sales_detail(self, record_id, **kw):
        record = request.env['pre.sales'].sudo().browse(record_id)
        if not record.exists() or record.user_id.id != request.env.user.id:
            return request.render('website.403')
        return request.render('pre_sales.pre_sales_portal_detail', {'record': record})

    @http.route(['/my/pre_sales/new'], type='http', auth='user', methods=['GET', 'POST'], website=True, csrf=True)
    def portal_pre_sales_new(self, **post):
        PreSales = request.env['pre.sales'].sudo()
        # companies=request.env['res.compnay'].sudo().search[()]

        # users=request.env['res.user'].sudo().search(
        #                                            )

        if request.httprequest.method == 'POST':
            try:
                vals = {
                    'user_id': request.env.user.id,
                    'SBUs': int(post.get('SBUs')) if post.get('SBUs') else request.env.company.id,
                    'date': post.get('date'),
                   
                    'country': post.get('country'),
                    'profile_name': int(post.get('profile_name')) if post.get('profile_name') else False,
                    'biding_amount': float(post.get('biding_amount') or 0.0),
                    'amount_status': post.get('amount_status'),
                    'client_category': post.get('client_category'),
                    'quote_category': post.get('quote_category'),
                    'service_type':post.get('service_type'),
             
                }
                record = PreSales.create(vals)
                return request.redirect(f'/my/pre_sales/{record.id}')
            except Exception as e:
                # Handle errors
                companies = request.env['res.company'].sudo().search([])
                profiles = request.env['hr.employee'].sudo().search([])
                return request.render('pre_sales.pre_sales_portal_new', {
                    'companies': companies,
                    'profiles': profiles,
                    'error': str(e),
                    'form_data': post,
                })

        companies = request.env['res.company'].sudo().search([])
        profiles = request.env['hr.employee'].sudo().search([])

        return request.render('pre_sales.pre_sales_portal_new', {
            'companies': companies,
            'profiles': profiles,
        })