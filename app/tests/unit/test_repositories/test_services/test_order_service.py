import pytest
from unittest.mock import Mock, AsyncMock, patch  # Добавляем импорт
from app.services.order_service import OrderService
from uuid import uuid4

class TestOrderService:
    
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""
        # Мокаем репозитории
        mock_order_repo = AsyncMock()
        mock_product_repo = AsyncMock()
        mock_user_repo = AsyncMock()
        
        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(id=1, email="test@example.com")
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", price=100.0, stock_quantity=5
        )
        mock_order_repo.create.return_value = Mock(
            id=uuid4(), user_id=1, total_amount=200.0, status="pending"
        )
        
        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo
        )
        
        order_data = {
            "user_id": 1,
            "items": [{"product_id": 1, "quantity": 2}]
        }
        
        result = await order_service.create_order(order_data)
        
        assert result is not None
        assert result["total_amount"] == 200.0
        mock_order_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        """Тест создания заказа с недостаточным количеством товара"""
        mock_order_repo = AsyncMock()
        mock_product_repo = AsyncMock()
        mock_user_repo = AsyncMock()
        
        mock_user_repo.get_by_id.return_value = Mock(id=1)
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", price=100.0, stock_quantity=1
        )
        
        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo
        )
        
        order_data = {
            "user_id": 1,
            "items": [{"product_id": 1, "quantity": 5}]  # Заказываем больше чем есть
        }
        
        with pytest.raises(ValueError, match="Insufficient stock"):
            await order_service.create_order(order_data)