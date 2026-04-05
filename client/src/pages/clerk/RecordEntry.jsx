import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';

// Changed for new store_products junction table: use store_product_id instead of product_id
const RecordEntry = () => {
  const navigate = useNavigate();
  const [storeProducts, setStoreProducts] = useState([]);   // Changed: now fetching store_products instead of products
  const [submitting, setSubmitting] = useState(false);
  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm({
    defaultValues: {
      quantity_spoilt: 0,
      payment_status: 'unpaid'
    }
  });

  useEffect(() => {
    const fetchStoreProducts = async () => {
      try {
        const res = await api.get('/store-products/');   // Changed for new schema
        setStoreProducts(res.data.store_products || []);
      } catch (err) {
        toast.error(err.response?.data?.error || 'Failed to load products');
      }
    };
    fetchStoreProducts();
  }, []);

  const qtyReceived = watch('quantity_received');

  const onSubmit = async (data) => {
    setSubmitting(true);
    try {
      await api.post('/inventory/', data);
      toast.success('Entry recorded successfully ✅');
      reset();
      navigate('/clerk/my-entries');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to record entry');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <DashboardLayout title="Record New Entry 📝">
      <div className="max-w-2xl mx-auto">
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Store Product *
              </label>
              <select
                className="input-field"
                {...register('store_product_id', { required: 'Please select a product' })}
              >
                <option value="">Select a product in this store...</option>
                {storeProducts.map((sp) => (
                  <option key={sp.id} value={sp.id}>
                    {sp.product_name}
                  </option>
                ))}
              </select>
              {errors.store_product_id && (
                <p className="text-red-500 text-sm mt-1">{errors.store_product_id.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="relative">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Qty Received *
                </label>
                <input
                  type="number"
                  min="0"
                  className={`input-field ${errors.quantity_received ? 'border-red-500' : ''}`}
                  {...register('quantity_received', { 
                    required: 'Required', 
                    min: { value: 1, message: 'Must be > 0' },
                    valueAsNumber: true 
                  })}
                />
                {errors.quantity_received && <p className="text-red-500 text-xs mt-1">{errors.quantity_received.message}</p>}
              </div>
              <div className="relative">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Qty In Stock *
                </label>
                <input
                  type="number"
                  min="0"
                  className={`input-field ${errors.quantity_in_stock ? 'border-red-500' : ''}`}
                  {...register('quantity_in_stock', { 
                    required: 'Required',
                    valueAsNumber: true,
                    validate: (value) => 
                      value <= (qtyReceived || 0) || 'Cannot exceed received'
                  })}
                />
                {errors.quantity_in_stock && <p className="text-red-500 text-xs mt-1">{errors.quantity_in_stock.message}</p>}
              </div>
              <div className="relative">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Qty Spoilt
                </label>
                <input
                  type="number"
                  min="0"
                  className={`input-field ${errors.quantity_spoilt ? 'border-red-500' : ''}`}
                  {...register('quantity_spoilt', { 
                    valueAsNumber: true,
                    validate: (value) => {
                      const inStock = watch('quantity_in_stock') || 0;
                      return (value + inStock) <= (qtyReceived || 0) || 'Sum exceeds received qty';
                    }
                  })}
                />
                {errors.quantity_spoilt && <p className="text-red-500 text-xs mt-1">{errors.quantity_spoilt.message}</p>}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Buying Price (KES) *
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className="input-field"
                  {...register('buying_price', { required: 'Required', min: 0, valueAsNumber: true })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Selling Price (KES) *
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className="input-field"
                  {...register('selling_price', { required: 'Required', min: 0, valueAsNumber: true })}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Payment Status
              </label>
              <select
                className="input-field"
                {...register('payment_status')}
              >
                <option value="unpaid">Unpaid</option>
                <option value="paid">Paid</option>
              </select>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-6">
              <button
                type="submit"
                disabled={submitting}
                className="btn-primary disabled:opacity-50 flex-1 py-3 text-base font-medium"
              >
                {submitting ? 'Recording Entry...' : 'Record Entry ✅'}
              </button>
              <button
                type="button"
                onClick={() => navigate('/clerk/dashboard')}
                className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 text-sm font-medium"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default RecordEntry;
