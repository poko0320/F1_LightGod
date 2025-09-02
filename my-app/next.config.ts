const nextConfig = {
  experimental: {
    // Allow opening the dev server from these origins
    allowedDevOrigins: [
      'http://192.168.1.122:3000', // the device/IP you use
      'http://localhost:3000',     // keep localhost too
    ],
  },
};

module.exports = nextConfig;