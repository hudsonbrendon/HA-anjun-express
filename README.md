# Anjun Express Integration for Home Assistant

A custom Home Assistant integration to track packages from Anjun Express shipping company.

## Features

- **Real-time Package Tracking**: Monitor your Anjun Express packages directly from Home Assistant
- **Multiple Sensors**: Get detailed information about your packages:
  - Current delivery status
  - Current location
  - Last update timestamp
  - Number of tracking events
  - Delivery confirmation (binary sensor)
- **Multilingual Support**: Available in English and Portuguese (Brazil)
- **Easy Setup**: Simple configuration through the Home Assistant UI

## Installation

### Manual Installation

1. Copy the `custom_components/anjun_express` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click the "+" button and search for "Anjun Express"
5. Enter your tracking number and a name for your package

## Configuration

The integration requires:
- **Tracking Number**: Your Anjun Express tracking code (e.g., AJ250507242061301)
- **Package Name**: A friendly name for your package (e.g., "My Order")

## Sensors

### Current Status
Shows the current delivery status of your package.

### Current Location
Shows the current location/address of your package.

### Last Update
Shows when the package information was last updated.

### Tracking Events
Shows the total number of tracking events and includes detailed event history in attributes.

### Delivered (Binary Sensor)
Indicates whether the package has been delivered.

## API Information

This integration uses the Anjun Express tracking API:
- **Endpoint**: `https://website-trackings.anjunexpress.com.br/tracking/get-tracking`
- **Update Interval**: 30 minutes (configurable)

## Supported Status Messages

The integration recognizes various delivery status messages in both Portuguese and English, including:
- Package movements between distribution centers
- Arrival at delivery points
- Out for delivery
- Delivery confirmation

## Example Package Tracking

When you add a package, you'll get entities like:
- `sensor.my_package_current_status` - Shows "Objeto saiu para entrega ao destinatário"
- `sensor.my_package_current_location` - Shows "Parnamirim / RN"
- `sensor.my_package_last_update` - Shows the timestamp of last update
- `sensor.my_package_tracking_events` - Shows number of events with full history in attributes
- `binary_sensor.my_package_delivered` - Shows if package is delivered

## Development

To set up the development environment:

1. Open this repository in Visual Studio Code with the Dev Container extension
2. The container will automatically set up the development environment
3. Run `scripts/develop` to start Home Assistant with the integration loaded
4. Go to `localhost:8123` to access the Home Assistant instance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
