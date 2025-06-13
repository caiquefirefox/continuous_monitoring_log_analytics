#!/usr/bin/env python3
"""
Jaeger Tracing Demo 2025 - Aplicação Python Modernizada
Demonstra distributed tracing com OpenTelemetry e Jaeger
"""

import time
import random
import logging
from typing import Dict, Any
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModernTracingApp:
    def __init__(self):
        self.setup_tracing()
        self.tracer = trace.get_tracer(__name__)
        
    def setup_tracing(self):
        """Configura OpenTelemetry com Jaeger"""
        resource = Resource.create({
            ResourceAttributes.SERVICE_NAME: "python-microservice",
            ResourceAttributes.SERVICE_VERSION: "2.0.0",
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development",
            "team": "monitoring",
            "component": "backend"
        })
        
        # Configurar TracerProvider
        trace.set_tracer_provider(TracerProvider(resource=resource))
        
        # Configurar Jaeger Exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="jaeger",
            agent_port=6831,
        )
        
        # Configurar Span Processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        
        # Instrumentar requests automaticamente
        RequestsInstrumentor().instrument()
        
        logger.info("🚀 OpenTelemetry configurado com sucesso!")

    def simulate_user_journey(self) -> Dict[str, Any]:
        """Simula uma jornada completa do usuário"""
        with self.tracer.start_as_current_span("user_journey") as span:
            span.set_attribute("user.id", f"user_{random.randint(1000, 9999)}")
            span.set_attribute("user.type", random.choice(["premium", "basic", "trial"]))
            
            # Simular autenticação
            auth_result = self.authenticate_user(span)
            
            # Processar pedido
            if auth_result["success"]:
                order_result = self.process_order(span)
                payment_result = self.process_payment(span, order_result["amount"])
                notification_result = self.send_notification(span, order_result["order_id"])
                
                result = {
                    "journey_id": f"journey_{int(time.time())}",
                    "success": payment_result["success"],
                    "order": order_result,
                    "payment": payment_result,
                    "notification": notification_result
                }
            else:
                result = {"journey_id": f"journey_{int(time.time())}", "success": False, "error": "authentication_failed"}
            
            span.set_attribute("journey.success", result["success"])
            return result

    def authenticate_user(self, parent_span) -> Dict[str, Any]:
        """Simula autenticação de usuário"""
        with self.tracer.start_as_current_span("authenticate_user", parent_span) as span:
            span.set_attribute("auth.method", "oauth2")
            
            # Simular latência de autenticação
            auth_delay = random.uniform(0.1, 0.5)
            time.sleep(auth_delay)
            
            # Simular falha ocasional
            success = random.random() > 0.1  # 90% success rate
            
            span.set_attribute("auth.success", success)
            span.set_attribute("auth.latency_ms", auth_delay * 1000)
            
            if not success:
                span.set_attribute("error", True)
                span.add_event("Authentication failed", {"reason": "invalid_credentials"})
                
            return {"success": success, "latency": auth_delay}

    def process_order(self, parent_span) -> Dict[str, Any]:
        """Simula processamento de pedido"""
        with self.tracer.start_as_current_span("process_order", parent_span) as span:
            order_id = f"order_{int(time.time())}{random.randint(100, 999)}"
            amount = round(random.uniform(10.0, 500.0), 2)
            items = random.randint(1, 5)
            
            span.set_attribute("order.id", order_id)
            span.set_attribute("order.amount", amount)
            span.set_attribute("order.items_count", items)
            span.set_attribute("order.currency", "USD")
            
            # Simular validação de estoque
            self.validate_inventory(span, items)
            
            # Simular cálculo de frete
            self.calculate_shipping(span, amount)
            
            processing_time = random.uniform(0.2, 1.0)
            time.sleep(processing_time)
            
            span.add_event("Order processed successfully", {
                "processing_time_ms": processing_time * 1000,
                "warehouse": random.choice(["east", "west", "central"])
            })
            
            return {"order_id": order_id, "amount": amount, "items": items}

    def validate_inventory(self, parent_span, items: int):
        """Simula validação de estoque"""
        with self.tracer.start_as_current_span("validate_inventory", parent_span) as span:
            span.set_attribute("inventory.items_requested", items)
            
            # Simular consulta ao banco
            db_time = random.uniform(0.05, 0.2)
            time.sleep(db_time)
            
            available = random.randint(items, items + 10)
            span.set_attribute("inventory.items_available", available)
            span.set_attribute("inventory.db_latency_ms", db_time * 1000)

    def calculate_shipping(self, parent_span, amount: float):
        """Simula cálculo de frete"""
        with self.tracer.start_as_current_span("calculate_shipping", parent_span) as span:
            shipping_cost = 0 if amount > 100 else round(random.uniform(5.0, 15.0), 2)
            
            span.set_attribute("shipping.cost", shipping_cost)
            span.set_attribute("shipping.free_threshold", 100.0)
            span.set_attribute("shipping.method", random.choice(["standard", "express", "overnight"]))
            
            time.sleep(random.uniform(0.1, 0.3))

    def process_payment(self, parent_span, amount: float) -> Dict[str, Any]:
        """Simula processamento de pagamento"""
        with self.tracer.start_as_current_span("process_payment", parent_span) as span:
            payment_method = random.choice(["credit_card", "debit_card", "paypal", "bank_transfer"])
            span.set_attribute("payment.method", payment_method)
            span.set_attribute("payment.amount", amount)
            
            # Simular gateway de pagamento
            gateway_response = self.call_payment_gateway(span, amount, payment_method)
            
            # Simular processamento
            processing_time = random.uniform(0.5, 2.0)
            time.sleep(processing_time)
            
            success = gateway_response["success"] and random.random() > 0.05  # 95% success
            
            span.set_attribute("payment.success", success)
            span.set_attribute("payment.gateway", gateway_response["gateway"])
            
            if success:
                transaction_id = f"txn_{int(time.time())}{random.randint(1000, 9999)}"
                span.set_attribute("payment.transaction_id", transaction_id)
                span.add_event("Payment processed successfully")
            else:
                span.set_attribute("error", True)
                span.add_event("Payment failed", {"reason": "insufficient_funds"})
                
            return {"success": success, "amount": amount, "method": payment_method}

    def call_payment_gateway(self, parent_span, amount: float, method: str) -> Dict[str, Any]:
        """Simula chamada para gateway de pagamento"""
        with self.tracer.start_as_current_span("payment_gateway_call", parent_span) as span:
            gateway = random.choice(["stripe", "paypal", "square", "adyen"])
            span.set_attribute("gateway.provider", gateway)
            span.set_attribute("gateway.endpoint", f"https://api.{gateway}.com/v1/charges")
            
            # Simular latência de rede
            network_latency = random.uniform(0.1, 0.8)
            time.sleep(network_latency)
            
            success = random.random() > 0.02  # 98% gateway success
            
            span.set_attribute("gateway.success", success)
            span.set_attribute("gateway.latency_ms", network_latency * 1000)
            
            return {"success": success, "gateway": gateway}

    def send_notification(self, parent_span, order_id: str) -> Dict[str, Any]:
        """Simula envio de notificação"""
        with self.tracer.start_as_current_span("send_notification", parent_span) as span:
            channels = ["email", "sms", "push"]
            channel = random.choice(channels)
            
            span.set_attribute("notification.channel", channel)
            span.set_attribute("notification.order_id", order_id)
            
            # Simular processamento
            time.sleep(random.uniform(0.1, 0.4))
            
            success = random.random() > 0.1  # 90% success
            span.set_attribute("notification.success", success)
            
            if success:
                span.add_event("Notification sent successfully")
            else:
                span.set_attribute("error", True)
                span.add_event("Notification failed", {"reason": "service_unavailable"})
                
            return {"success": success, "channel": channel}

    def run_simulation(self):
        """Executa simulação contínua"""
        logger.info("🎯 Iniciando simulação de tracing...")
        
        simulation_count = 0
        while True:
            try:
                simulation_count += 1
                
                with self.tracer.start_as_current_span("simulation_cycle") as span:
                    span.set_attribute("simulation.cycle", simulation_count)
                    
                    # Simular diferentes padrões de tráfego
                    if simulation_count % 10 == 0:
                        # Simular pico de tráfego
                        span.add_event("Traffic spike detected")
                        for _ in range(3):
                            result = self.simulate_user_journey()
                            time.sleep(0.5)
                    else:
                        # Tráfego normal
                        result = self.simulate_user_journey()
                    
                    # Log resultado
                    logger.info(f"Ciclo {simulation_count}: Journey {'✅ Sucesso' if result.get('success') else '❌ Falha'}")
                
                # Pausa entre simulações
                sleep_time = random.uniform(2, 8)
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                logger.info("🛑 Simulação interrompida pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro na simulação: {e}")
                time.sleep(5)

def main():
    """Função principal"""
    print("🚀 Jaeger Tracing Demo 2025")
    print("=" * 50)
    print("🔍 Distributed Tracing com OpenTelemetry")
    print("📊 Jaeger UI: http://localhost:16686")
    print("🌐 HotROD App: http://localhost:8080")
    print("📈 Prometheus: http://localhost:9090")
    print("📊 Grafana: http://localhost:3000")
    print("=" * 50)
    
    app = ModernTracingApp()
    app.run_simulation()

if __name__ == "__main__":
    main()

