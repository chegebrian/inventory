import React, { useEffect, useState, useCallback } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', description: '', store_id: '' });
  const [stores, setStores] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get(`/products/?page=${page}&per_page=10`);
      setProducts(res.data.products || []);
      setTotalPages(res.data.pages || 1);
    } catch {
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  }, [page]);

  const fetchStores = useCallback(async () => {
    try {
      const res = await api.get('/stores/');
      setStores(res.data.stores || []);
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    fetchProducts();
    fetchStores();
  }, [fetchProducts, fetchStores]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.store_id) {
      return toast.error('Name and Store are required');
    }

    try {
      await api.post('/products/', form);
      toast.success('Product created successfully ✅');
      setShowForm(false);
      setForm({ name: '', description: '', store_id: '' });
      fetchProducts();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to create product');
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Delete product "${name}"?`)) return;

    try {
      await api.delete(`/products/${id}`);
      toast.success('Product deleted');
      fetchProducts();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to delete product');
    }
  };

  const getStoreName = (storeId) => {
    const store = stores.find(s => s.id === storeId);
    return store ? store.name : `Store #${storeId}`;
  };

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <DashboardLayout title="Products 📦">
      <div>Admin Products</div>
    </DashboardLayout>
  );
};

export default AdminProducts;