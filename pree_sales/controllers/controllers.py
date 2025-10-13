from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import json


class BiddingPortal(CustomerPortal):

    @http.route(['/my/bidding'], type='http', auth='user', website=True)
    def portal_my_bidding(self, **kw):
        """Bidding list page"""
        partner = request.env.user.partner_id

        # Get all bidding records for current user
        bidding_records = request.env['res.partner'].search([
            ('create_uid', '=', request.env.uid)
        ])

        values = {
            'bidding_records': bidding_records,
            'page_name': 'bidding',
        }
        return request.render("pree_sales.portal_my_bidding", values)

    @http.route(['/my/bidding/create'], type='http', auth='user', website=True)
    def portal_bidding_create(self, **kw):
        """Bidding create form page"""
        values = {
            'page_name': 'bidding_create',
        }
        return request.render("pree_sales.portal_bidding_create_form", values)

    @http.route(['/my/bidding/submit'], type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def portal_bidding_submit(self, **post):
        """Submit bidding data"""
        try:
            partner = request.env.user.partner_id

            # Create new partner record with bidding data
            vals = {
                'name': post.get('client_name', ''),
                'bidding_amount': post.get('bidding_amount', ''),
                'client_user': post.get('client_user', ''),
                'user_code': post.get('user_code', ''),
                'client_name': post.get('client_name', ''),
                'Sbus_id': post.get('Sbus_id', ''),
                'date': post.get('date', ''),
                'Service_type': post.get('Service_type', ''),
                'bidding_status': post.get('bidding_status', 'draft'),
                'payment_status': post.get('payment_status', ''),
                'client_category': post.get('client_category', ''),
                'quote_category': post.get('quote_category', ''),
                'profile': post.get('profile', ''),
            }

            # Create record
            new_bidding = request.env['res.partner'].sudo().create(vals)

            return request.redirect('/my/bidding?message=success')

        except Exception as e:
            return request.redirect('/my/bidding/create?error=' + str(e))

    @http.route(['/my/bidding/<int:bidding_id>'], type='http', auth='user', website=True)
    def portal_bidding_detail(self, bidding_id, **kw):
        """Bidding detail page"""
        bidding = request.env['res.partner'].browse(bidding_id)

        # Check access rights
        if not bidding.exists() or bidding.create_uid.id != request.env.uid:
            return request.redirect('/my')

        values = {
            'bidding': bidding,
            'page_name': 'bidding_detail',
        }
        return request.render("pree_sales.portal_bidding_detail", values)

    @http.route(['/my/bidding/edit/<int:bidding_id>'], type='http', auth='user', website=True)
    def portal_bidding_edit(self, bidding_id, **kw):
        """Bidding edit form"""
        bidding = request.env['res.partner'].browse(bidding_id)

        # Check access rights
        if not bidding.exists() or bidding.create_uid.id != request.env.uid:
            return request.redirect('/my')

        values = {
            'bidding': bidding,
            'page_name': 'bidding_edit',
        }
        return request.render("pree_sales.portal_bidding_edit_form", values)

    @http.route(['/my/bidding/update/<int:bidding_id>'], type='http', auth='user', website=True, methods=['POST'],
                csrf=True)
    def portal_bidding_update(self, bidding_id, **post):
        """Update bidding data"""
        try:
            bidding = request.env['res.partner'].browse(bidding_id)

            # Check access rights
            if not bidding.exists() or bidding.create_uid.id != request.env.uid:
                return request.redirect('/my')

            vals = {
                'bidding_amount': post.get('bidding_amount', ''),
                'client_user': post.get('client_user', ''),
                'user_code': post.get('user_code', ''),
                'client_name': post.get('client_name', ''),
                'Sbus_id': post.get('Sbus_id', ''),
                'date': post.get('date', ''),
                'Service_type': post.get('Service_type', ''),
                'bidding_status': post.get('bidding_status', 'draft'),
                'payment_status': post.get('payment_status', ''),
                'client_category': post.get('client_category', ''),
                'quote_category': post.get('quote_category', ''),
                'profile': post.get('profile', ''),
            }

            bidding.sudo().write(vals)

            return request.redirect(f'/my/bidding/{bidding_id}?message=updated')

        except Exception as e:
            return request.redirect(f'/my/bidding/edit/{bidding_id}?error=' + str(e))

    @http.route(['/my/bidding/delete/<int:bidding_id>'], type='http', auth='user', website=True, csrf=True)
    def portal_bidding_delete(self, bidding_id, **kw):
        """Delete bidding record"""
        try:
            bidding = request.env['res.partner'].browse(bidding_id)

            # Check access rights
            if not bidding.exists() or bidding.create_uid.id != request.env.uid:
                return request.redirect('/my')

            bidding.sudo().unlink()

            return request.redirect('/my/bidding?message=deleted')

        except Exception as e:
            return request.redirect('/my/bidding?error=' + str(e))