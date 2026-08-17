# AgriMarket Testing Guide

## Initial Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python run.py seed_admin
```

4. Run the application:
```bash
python run.py
```

Visit: http://localhost:5000

## Test Scenarios

### 1. Admin Flow

**Login as Admin:**
- Email: admin@agrimarket.com
- Password: admin123

**Test Admin Features:**
1. View dashboard with platform statistics
2. Navigate to User Management
3. View all users (farmers and buyers)
4. Check pending farmer verifications
5. Broadcast a notification to all users

### 2. Farmer Registration & Setup

**Register as Farmer:**
1. Click "Register" → Select "Farmer" role
2. Fill in details:
   - Name: John Farmer
   - Email: farmer@test.com
   - Password: test123
   - Phone: 9876543210
   - Address, City, State, Pincode
3. Submit registration
4. Note: Account pending admin approval

**Admin Approves Farmer:**
1. Login as admin
2. Go to User Management → Filter by Farmers
3. Click "Verify" on John Farmer's account

**Farmer Login & Add Products:**
1. Login as farmer@test.com / test123
2. View dashboard (should show 0 products, 0 orders)
3. Navigate to "Products" → "Add Product"
4. Add product:
   - Name: Fresh Tomatoes
   - Category: Vegetables
   - Price: 50 per kg
   - Stock: 100 kg
   - Min Order: 5 kg
   - Enable bulk: Yes, Bulk price: 45, Min bulk: 50 kg
   - Upload image (optional)
5. Add more products (Potatoes, Onions, etc.)

### 3. Buyer Registration & Shopping

**Register as Buyer:**
1. Click "Register" → Select "Buyer" role
2. Fill in details:
   - Name: Jane Buyer
   - Email: buyer@test.com
   - Password: test123
   - Phone: 9876543211
   - Address details
3. Submit (buyers are auto-verified)

**Browse & Order:**
1. Login as buyer@test.com / test123
2. Navigate to "Products"
3. Browse products, use search and filters
4. Click on a product to view details
5. Add to cart (quantity: 10 kg)
6. View cart
7. Proceed to checkout
8. Enter delivery address
9. Place order

### 4. Order Management

**Farmer Processes Order:**
1. Login as farmer
2. Check dashboard (should show 1 active order)
3. Navigate to "Orders"
4. Click "View" on the order
5. Click "Confirm Order"
6. Update status to "Processing"
7. Update status to "Shipped"
8. Update status to "Delivered"

**Buyer Tracks Order:**
1. Login as buyer
2. Navigate to "Orders"
3. Click "View" on the order
4. See order status progression
5. View order details and items

### 5. Farmer Analytics

**View Analytics:**
1. Login as farmer
2. Navigate to "Analytics"
3. View daily sales chart
4. View top products chart
5. Check revenue and profit metrics

### 6. B2B Contracts

**Buyer Requests Contract:**
1. Login as buyer
2. Navigate to "B2B" → "Contracts"
3. Click "Request New Contract"
4. Select a bulk-available product
5. Enter:
   - Proposed price: 40 per kg
   - Volume: 500 kg
   - Start/End dates
   - Delivery schedule
6. Submit request

**Farmer Activates Contract:**
1. Login as farmer
2. Navigate to "B2B" → "Contracts"
3. View contract request
4. Click "Activate"
5. Enter advance payment received
6. Activate contract

### 7. Notifications

**Test Real-time Notifications:**
1. Open two browser windows
2. Login as farmer in one, buyer in another
3. Buyer places an order
4. Farmer should see notification (bell icon)
5. Click bell to view notifications
6. Mark as read

### 8. Messaging (if implemented)

**Send Messages:**
1. Login as buyer
2. Navigate to product detail page
3. Click "Message Farmer"
4. Send a message
5. Login as farmer
6. Check messages
7. Reply to buyer

### 9. Reports

**Generate Reports:**
1. Login as farmer
2. Navigate to "Reports"
3. View daily report
4. Click "Export PDF"
5. Click "Export Excel"
6. Download and verify files

### 10. Admin Management

**Admin Functions:**
1. Login as admin
2. View all orders across platform
3. View all products
4. Deactivate a user
5. Reactivate a user
6. Broadcast notification:
   - Title: "Platform Maintenance"
   - Message: "Scheduled maintenance tonight"
7. All users should receive notification

## Edge Cases to Test

### Stock Management
1. Farmer adds product with 10 kg stock
2. Buyer orders 8 kg → Stock should be 2 kg
3. Buyer tries to order 5 kg → Should fail (insufficient stock)

### Order Cancellation
1. Buyer places order (status: pending)
2. Buyer cancels order
3. Stock should be restored
4. Farmer should receive cancellation notification

### Bulk Pricing
1. Product: Regular price 50/kg, Bulk price 45/kg for 50+ kg
2. Buyer orders 30 kg → Price should be 50/kg
3. Buyer orders 60 kg → Price should be 45/kg

### Farmer Verification
1. New farmer registers
2. Try to login → Should show "pending approval" message
3. Admin verifies farmer
4. Farmer can now login and access dashboard

### Low Stock Alerts
1. Farmer adds product with 5 kg stock (below threshold of 10)
2. Dashboard should show low stock warning
3. Farmer should see alert

## API Testing (Optional)

### Notifications API
```bash
# Get notifications (requires authentication)
curl -X GET http://localhost:5000/notifications/

# Get unread count
curl -X GET http://localhost:5000/notifications/unread-count

# Mark as read
curl -X POST http://localhost:5000/notifications/mark-read/1
```

## Common Issues & Solutions

### Database Issues
```bash
# Reset database
rm agrimarket.db
flask db upgrade
python run.py seed_admin
```

### Port Already in Use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Performance Testing

### Load Testing (Optional)
```bash
# Install locust
pip install locust

# Create locustfile.py with test scenarios
# Run: locust -f locustfile.py
```

## Security Testing

1. Test SQL injection in search fields
2. Test XSS in product descriptions
3. Test CSRF protection on forms
4. Test file upload restrictions
5. Test authentication on protected routes

## Browser Compatibility

Test on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Checklist

- [ ] Admin can login and manage platform
- [ ] Farmers can register and get verified
- [ ] Farmers can add/edit/delete products
- [ ] Buyers can browse and search products
- [ ] Buyers can add to cart and checkout
- [ ] Orders are created correctly
- [ ] Stock is updated after orders
- [ ] Farmers can process orders
- [ ] Order status updates work
- [ ] Notifications are sent
- [ ] B2B contracts can be created
- [ ] Reports can be generated
- [ ] Analytics charts display correctly
- [ ] Profile updates work
- [ ] Password change works
- [ ] Error pages display correctly
- [ ] Responsive design works on mobile

## Next Steps

After testing:
1. Configure production environment
2. Set up email notifications
3. Integrate Razorpay payment gateway
4. Deploy to production server
5. Set up monitoring and logging
