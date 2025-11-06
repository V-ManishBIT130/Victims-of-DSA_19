import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config();

const connectDB = async () => {
  try {
    const mongoURL = process.env.mongo_url;
    
    if (!mongoURL) {
      throw new Error('MongoDB URL not found in environment variables');
    }

    await mongoose.connect(mongoURL);

    console.log('✅ MongoDB Connected Successfully');
    console.log(`📦 Database: ${mongoose.connection.db.databaseName}`);
  } catch (error) {
    console.error('❌ MongoDB Connection Error:', error.message);
    process.exit(1);
  }
};

// Handle connection events
mongoose.connection.on('disconnected', () => {
  console.log('⚠️  MongoDB Disconnected');
});

mongoose.connection.on('error', (err) => {
  console.error('❌ MongoDB Error:', err);
});

export default connectDB;
