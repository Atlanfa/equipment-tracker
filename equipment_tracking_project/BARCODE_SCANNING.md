# Equipment QC Tracking - Barcode Scanning Implementation

## Overview
Real barcode scanning functionality has been implemented using **QuaggaJS**, a JavaScript library for real-time barcode scanning in web browsers.

## Features Implemented

### 🔍 **Real Barcode Scanning**
- **Library**: QuaggaJS (CDN version 0.12.1)
- **Supported Formats**: Code 128, EAN, Code 39, UPC, Codabar, and more
- **Camera Access**: Uses device camera with environment facing mode (back camera)
- **Real-time Detection**: Continuous scanning with visual feedback

### 📱 **User Interface**
- **Scanner Viewport**: 400x300 pixel camera view with overlay canvas
- **Status Indicator**: Real-time status updates during scanning
- **Visual Feedback**: Green overlay when barcode is detected
- **Auto-search**: Automatically searches database after successful scan

### 🛠 **Fallback Options**
- **Manual Entry Button**: ⌨️ Manual Entry for typing barcodes
- **Error Handling**: Graceful fallback when camera is unavailable
- **Permission Handling**: Clear error messages for camera permission issues

## How to Use

### 1. **Access Warehouse Management**
- Click "Switch to Warehouse Management" button
- Navigate to the Equipment Location Finder section

### 2. **Start Barcode Scanning**
- Click "📷 Scan Barcode" button
- Allow camera permissions when prompted
- Position barcode within the blue frame
- Wait for automatic detection and processing

### 3. **Alternative Methods**
- **Search by name**: Type equipment name (e.g., "Laptop")
- **Manual barcode**: Click "⌨️ Manual Entry" and type barcode
- **Search by barcode**: Type barcode directly in search field

## Sample Barcodes for Testing

The system includes sample equipment with these barcodes:

| Equipment | Barcodes |
|-----------|----------|
| Laptop | LAP001, LAP002, LAP003, 123456789012 |
| Monitor | MON001, MON002, 234567890123 |
| Projector | PROJ001, 345678901234 |
| Camera | CAM001, CAM002, 456789012345 |
| Printer | PRT001, 567890123456 |
| Scanner | SCN001, 678901234567 |
| Tablet | TAB001, TAB002, TAB003, 789012345678 |
| Microphone | MIC001, MIC002, 890123456789 |

## Technical Implementation

### **Frontend (JavaScript)**
```javascript
// QuaggaJS initialization with multiple barcode formats
Quagga.init({
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#quagga-viewport'),
        constraints: {
            width: 400,
            height: 300,
            facingMode: "environment"
        }
    },
    decoder: {
        readers: [
            "code_128_reader", "ean_reader", "ean_8_reader",
            "code_39_reader", "upc_reader", "codabar_reader"
        ]
    }
});
```

### **Backend (Django)**
- **API Endpoint**: `/api/search-equipment/`
- **Search Logic**: Searches by equipment name and barcode
- **Database Models**: Equipment, Barcode, Location models
- **Response Format**: JSON with equipment details and locations

### **Database Structure**
```python
# Equipment with multiple barcodes and locations
Equipment -> Barcode (One-to-Many)
Equipment -> Location (Many-to-Many)
```

## Browser Compatibility

### **Supported Browsers**
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari (iOS/macOS)
- ✅ Edge

### **Requirements**
- **HTTPS**: Camera access requires secure connection
- **Permissions**: Camera access permission required
- **Hardware**: Device with camera (front/back)

## Troubleshooting

### **Common Issues**

1. **Camera Not Working**
   - Check browser permissions
   - Ensure HTTPS connection
   - Try different browser
   - Use manual entry fallback

2. **Barcode Not Detected**
   - Ensure good lighting
   - Hold barcode steady in frame
   - Try different distance/angle
   - Check barcode format compatibility

3. **No Search Results**
   - Verify barcode exists in database
   - Check spelling of equipment name
   - Use sample barcodes for testing

### **Development Setup**
```bash
# Run sample data population
python manage.py populate_sample_data

# Start development server
python manage.py runserver

# Access application
http://127.0.0.1:8000
```

## Security Considerations

- **Camera Access**: Only when explicitly requested by user
- **CSRF Protection**: All API calls include CSRF tokens
- **Error Handling**: No sensitive information in error messages
- **Permission Checks**: Graceful handling of denied permissions

## Future Enhancements

- **QR Code Support**: Add QR code scanning capability
- **Batch Scanning**: Scan multiple items in sequence
- **Offline Mode**: Cache for offline scanning
- **Export Data**: Export location data to CSV/PDF
- **Advanced Filters**: Filter by location, status, etc.

---

*Last Updated: July 6, 2025*
