#!/usr/bin/env python3
"""
RouterOS REST API 测试脚本

这个脚本用于测试修改后的RouterOSClient类是否正常工作，该类现在使用RouterOS REST API而不是传统API。

使用前请确保：
1. RouterOS设备已启用REST API服务
2. 用户名和密码具有足够的权限
3. 设备的IP地址、端口等信息正确

使用方法：
python3 routeros_rest_test.py --ros-ip 192.168.2.2 --ros-user admin --ros-pass password -p 8080
"""

import sys
import argparse
import logging
from natter import RouterOSClient, Logger

# 设置日志级别为DEBUG以查看详细信息
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_routeros_rest_api(args):
    """测试RouterOS REST API功能"""
    try:
        # 初始化RouterOSClient
        client = RouterOSClient(
            host=args.ros_ip,
            port=args.ros_port,
            username=args.ros_user,
            password=args.ros_pass,
            bind_ip=args.bind_ip,
            interface=args.interface,
            instance_id=args.instance_id
        )
        
        print("\n=== RouterOS REST API 测试开始 ===")
        
        # 测试获取接口名称
        print("\n1. 获取默认接口名称...")
        interface = client._get_interface_name()
        print(f"   成功获取接口名称: {interface}")
        
        # 测试删除现有规则
        print("\n2. 删除现有的Natter规则...")
        deleted = client.delete_all_natter_rules()
        print(f"   成功删除 {deleted} 条规则")
        
        # 测试添加转发规则
        print(f"\n3. 添加端口转发规则 (TCP {args.port} -> {args.dest_host}:{args.dest_port})...")
        success = client.forward(
            host="",
            port=args.port,
            dest_host=args.dest_host,
            dest_port=args.dest_port,
            udp=args.udp
        )
        
        if success:
            print("   端口转发规则添加成功!")
            
            # 测试renew功能：每隔3秒renew一次，重复3次
            print("\n4. 测试renew功能...")
            import time
            for i in range(3):
                print(f"   第{i+1}次renew...")
                renew_success = client.renew()  # renew方法不接受参数，会使用forward时保存的配置
                if renew_success:
                    print("      renew成功!")
                else:
                    print("      renew失败!")
                time.sleep(3)  # 等待3秒
            
            # 自动删除测试规则
            print("\n5. 自动删除测试规则...")
            deleted = client.delete_all_natter_rules()
            print(f"   成功删除 {deleted} 条测试规则")
        else:
            print("   端口转发规则添加失败!")
            print("   请检查错误日志以获取详细信息")
            print("   常见问题：")
            print("   - 确保RouterOS设备已启用REST API")
            print("   - 验证用户名和密码是否正确")
            print("   - 确认用户具有足够的权限")
            print("   - 检查接口名称是否正确")
        
        # 关闭连接
        client.close()
        print("\n=== RouterOS REST API 测试结束 ===")
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        print("详细错误信息:")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RouterOS REST API 测试脚本')
    parser.add_argument('--ros-ip', required=True, help='RouterOS设备IP地址')
    parser.add_argument('--ros-port', type=int, default=80, help='RouterOS REST API端口 (默认: 80)')
    parser.add_argument('--ros-user', required=True, help='RouterOS用户名')
    parser.add_argument('--ros-pass', required=True, help='RouterOS密码')
    parser.add_argument('-p', '--port', type=int, default=8080, help='要转发的外部端口 (默认: 8080)')
    parser.add_argument('--dest-host', default='192.168.2.100', help='目标主机IP地址 (默认: 192.168.2.100)')
    parser.add_argument('--dest-port', type=int, default=80, help='目标主机端口 (默认: 80)')
    parser.add_argument('--udp', action='store_true', help='使用UDP协议 (默认使用TCP)')
    parser.add_argument('--bind-ip', help='绑定的本地IP地址')
    parser.add_argument('-i', '--interface', help='使用的网络接口')
    parser.add_argument('--instance-id', help='实例唯一标识，用于区分多个natter服务')
    
    args = parser.parse_args()
    
    # 显示配置信息
    print("\n=== 配置信息 ===")
    print(f"RouterOS IP: {args.ros_ip}")
    print(f"RouterOS REST API端口: {args.ros_port}")
    print(f"用户名: {args.ros_user}")
    print(f"端口转发: {args.port}->{args.dest_host}:{args.dest_port} ({'UDP' if args.udp else 'TCP'})")
    
    if args.bind_ip:
        print(f"绑定IP: {args.bind_ip}")
    if args.interface:
        print(f"网络接口: {args.interface}")
    if args.instance_id:
        print(f"实例标识: {args.instance_id}")
    
    # 开始测试
    test_routeros_rest_api(args)


if __name__ == '__main__':
    main()