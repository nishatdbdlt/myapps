from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class PortalBidding(http.Controller):

    @http.route(['/my/biddings'], type='http', auth='user', website=True)
    def portal_bidding_list(self, **kwargs):
        """Display list of bidding records for logged-in user"""
        # Get logged-in user
        user = request.env.user
        _logger.info(f"User accessing biddings: {user.name} (ID: {user.id})")

        # Search res.partner records assigned to this user
        partners = request.env['res.partner'].sudo().search([
            ('client_user_id', '=', user.id)
        ])

        _logger.info(f"Found {len(partners)} bidding records for user {user.id}")

        # Log each partner for debugging
        for partner in partners:
            _logger.info(f"Partner: {partner.name}, Amount: {partner.bidding_amount}, Status: {partner.bidding_status}")

        # Render template
        return request.render('pree_sales.portal_bidding_list', {
            'partners': partners,
        })

    @http.route(['/my/bidding/create'], type='http', auth='user', website=True)
    def portal_bidding_form(self, **kwargs):
        """Display bidding creation form"""
        _logger.info(f"User {request.env.user.name} accessing create form")
        return request.render('pree_sales.portal_bidding_form', {})

    @http.route(['/my/bidding/submit'], type='http', auth='user', website=True, methods=['POST'])
    def portal_bidding_submit(self, **post):
        """Handle bidding form submission"""
        user = request.env.user
        _logger.info(f"Bidding submission by {user.name}: {post}")

        try:
            # Create new partner record
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'bidding_amount': float(post.get('bidding_amount', 0)),
                'bidding_status': post.get('bidding_status', 'draft'),
                'client_user_id': user.id,
            })

            _logger.info(f"Created bidding record ID: {partner.id}")

        except Exception as e:
            _logger.error(f"Error creating bidding: {str(e)}")

        return request.redirect('/my/biddings')