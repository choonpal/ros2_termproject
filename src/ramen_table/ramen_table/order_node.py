# 이 노드는 터미널에서 입력을 받아 주문을 생성하고 /new_order 토픽으로 전송합니다.
# 실제 UI 대신 간단한 터미널 입력으로 주문을 시뮬레이션합니다.

import rclpy
from rclpy.node import Node
from ramen_interfaces.msg import RamenOrder
topping_dir={"x":0,"치즈":500,"떡":500,"만두":1000,"계란":500,"파":300,"김치":1000,"콩나물":500,"햄":1000,"고추":300}
side_dir={"음료":2000,"김밥":3000,"튀김":2000,"떡볶이":4000,"순대":3000,"어묵":3000}

class OrderNode(Node):
    def __init__(self):
        super().__init__('order_node')
        self.publisher_ = self.create_publisher(RamenOrder, 'new_order', 10)
        self.get_logger().info('--- 라면 주문 시스템 (Table) ---')
        self.send_test_order()
    
    def send_test_order(self):
        # TODO: 실제 UI나 터미널 입력을 통해 이 데이터를 받아야 합니다.
        # 여기서는 하드코딩된 테스트 주문을 사용합니다.
        
        table_num = int(input("테이블 번호를 입력하세요 (1-9): ") or "1")
        ramen_type = input("라면 종류를 입력하세요 (예: 신라면): ") or "신라면"
        
        # 복수 입력 처리
        toppings = input("토핑을 입력하세요 (콤마로 구분, 예: 치즈,떡): ")
        toppings_list = [t.strip() for t in toppings.split(',')] if toppings else []
        
        sides = input("사이드를 입력하세요 (콤마로 구분, 예: 콜라,김밥): ")
        sides_list = [s.strip() for s in sides.split(',')] if sides else []

        msg = RamenOrder()
        msg.table_number = table_num
        msg.ramen_type = ramen_type
        msg.toppings = toppings_list
        msg.sides = sides_list

        self.publisher_.publish(msg)
        self.get_logger().info(f'테이블 {msg.table_number}에서 주문 전송:')
        self.get_logger().info(f' - 라면: {msg.ramen_type}')
        self.get_logger().info(f' - 토핑: {", ".join(msg.toppings)}')
        self.get_logger().info(f' - 사이드: {", ".join(msg.sides)}')
        self.get_logger().info('---------------------------------')
        msg.price = self.calculate_price(toppings_list, sides_list)
        self.get_logger().info(f' - 총 가격: {msg.price}원')
    def calculate_price(self,toppings_list, sides_list):
        base_price = 3000  # 기본 라면 가격
        topping_price = sum(topping_dir[t] for t in toppings_list if t in topping_dir) # 토핑당 가격
        side_price = sum(side_dir[s] for s in sides_list if s in side_dir)  # 사이드당 가격
        return base_price + topping_price + side_price

def main(args=None):
    rclpy.init(args=args)
    order_node = OrderNode()
    # 주문을 한 번 보내고 종료되도록 설정 (시뮬레이션을 위해)
    # 실제 시스템에서는 UI가 켜져있는 동안 계속 실행되어야 함
    rclpy.spin_once(order_node)
    order_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
