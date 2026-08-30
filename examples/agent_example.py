#!/usr/bin/env python3
"""
AgentNexus Agent 接入示例脚本（T8.4）

演示一个外部Agent如何接入AgentNexus协同看板：
1. 注册到看板（/api/agents/register）
2. 启动webhook服务器接收@消息推送
3. 处理消息并回复（/api/messages）

用法：
    python3 agent_example.py --agent-id my-agent --agent-name "我的Agent" --port 9000

依赖：仅Python标准库（零依赖）
"""

import json
import time
import argparse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request


# ===== 配置 =====
DEFAULT_BOARD_URL = "http://localhost:8766"
DEFAULT_PROJECT = "collab-board-dev"


class AgentClient:
    """Agent客户端：注册、心跳、发消息"""

    def __init__(self, agent_id, agent_name, agent_role="", board_url=DEFAULT_BOARD_URL, project=DEFAULT_PROJECT):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.board_url = board_url.rstrip("/")
        self.project = project
        self.webhook_url = None
        self.registered = False

    def _api_url(self, path):
        """构建API URL，自动添加project参数"""
        separator = "&" if "?" in path else "?"
        return f"{self.board_url}{path}{separator}project={self.project}"

    def register(self, webhook_url):
        """注册Agent到看板

        Args:
            webhook_url: 接收@消息推送的webhook URL（如 http://localhost:9000/webhook）

        Returns:
            (success, message)
        """
        self.webhook_url = webhook_url
        entry = {
            "type": "http",
            "target": webhook_url
        }
        payload = {
            "agent_id": self.agent_id,
            "entry": entry
        }
        try:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                self._api_url("/api/agents/register"),
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("ok"):
                    self.registered = True
                    print(f"✅ Agent注册成功: {self.agent_name} ({self.agent_id})")
                    print(f"   Webhook: {webhook_url}")
                    return True, "注册成功"
                else:
                    return False, result.get("error", "注册失败")
        except Exception as e:
            return False, f"注册异常: {str(e)}"

    def heartbeat(self):
        """心跳：更新last_seen（接通确认）

        建议每30秒调用一次，保持在线状态。
        """
        if not self.registered:
            return False
        entry = {
            "type": "http",
            "target": self.webhook_url
        }
        payload = {
            "agent_id": self.agent_id,
            "entry": entry
        }
        try:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                self._api_url("/api/agents/register"),
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("ok", False)
        except Exception as e:
            print(f"⚠️  心跳失败: {e}")
            return False

    def send_message(self, content):
        """发送消息到看板

        Args:
            content: 消息内容

        Returns:
            (success, message_id)
        """
        payload = {
            "sender": self.agent_id,
            "content": content,
            "type": "text"
        }
        try:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                self._api_url("/api/messages"),
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("ok"):
                    return True, result.get("message_id")
                return False, None
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
            return False, None

    def claim_task(self, task_id):
        """认领任务

        Args:
            task_id: 任务ID

        Returns:
            success
        """
        payload = {
            "task_id": task_id,
            "assignee": self.agent_id
        }
        try:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                self._api_url("/api/claim"),
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("ok", False)
        except Exception as e:
            print(f"❌ 认领任务失败: {e}")
            return False


class WebhookHandler(BaseHTTPRequestHandler):
    """Webhook处理器：接收@消息推送"""

    agent_client = None  # 由外部设置

    def do_POST(self):
        if self.path == "/webhook":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                event = payload.get("event")
                msg = payload.get("message", {})

                if event == "message.mention":
                    sender = msg.get("sender", "unknown")
                    content = msg.get("content", "")
                    print(f"\n📩 收到@消息 (来自 {sender}):")
                    print(f"   {content[:100]}...")

                    # 处理消息（这里是示例，实际Agent可以在这里做自己的逻辑）
                    self.process_message(sender, content)

            except json.JSONDecodeError:
                pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        else:
            self.send_response(404)
            self.end_headers()

    def process_message(self, sender, content):
        """处理收到的@消息

        这是示例处理逻辑，实际Agent应该在这里做自己的任务处理。
        """
        if not self.agent_client:
            return

        # 简单回复示例
        reply = f"收到！我是 {self.agent_client.agent_name}，正在处理你的消息：{content[:50]}..."
        success, msg_id = self.agent_client.send_message(reply)
        if success:
            print(f"✅ 已回复 (message_id={msg_id})")

    def log_message(self, format, *args):
        """静默日志，不打印HTTP请求日志"""
        pass


def start_heartbeat(agent_client, interval=30):
    """启动心跳线程"""
    def heartbeat_loop():
        while True:
            time.sleep(interval)
            agent_client.heartbeat()
    t = threading.Thread(target=heartbeat_loop, daemon=True)
    t.start()
    print(f"💓 心跳已启动（每{interval}秒一次）")


def main():
    parser = argparse.ArgumentParser(description="AgentNexus Agent 接入示例")
    parser.add_argument("--agent-id", default="example-agent", help="Agent ID（唯一标识）")
    parser.add_argument("--agent-name", default="示例Agent", help="Agent显示名称")
    parser.add_argument("--agent-role", default="示例角色", help="Agent角色描述")
    parser.add_argument("--board-url", default=DEFAULT_BOARD_URL, help="看板服务器URL")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="项目名")
    parser.add_argument("--port", type=int, default=9000, help="Webhook监听端口")
    args = parser.parse_args()

    print("=" * 60)
    print("  AgentNexus Agent 接入示例")
    print("=" * 60)
    print(f"  Agent ID: {args.agent_id}")
    print(f"  Agent 名称: {args.agent_name}")
    print(f"  看板: {args.board_url}")
    print(f"  项目: {args.project}")
    print(f"  Webhook端口: {args.port}")
    print("=" * 60)

    # 1. 创建Agent客户端
    agent = AgentClient(
        agent_id=args.agent_id,
        agent_name=args.agent_name,
        agent_role=args.agent_role,
        board_url=args.board_url,
        project=args.project
    )

    # 2. 启动webhook服务器
    webhook_url = f"http://localhost:{args.port}/webhook"
    WebhookHandler.agent_client = agent
    server = HTTPServer(("0.0.0.0", args.port), WebhookHandler)
    print(f"\n🌐 Webhook服务器已启动: {webhook_url}")

    # 3. 注册Agent到看板
    print(f"\n🔗 正在注册Agent到看板...")
    success, msg = agent.register(webhook_url)
    if not success:
        print(f"❌ 注册失败: {msg}")
        print("提示：请确保看板服务器已启动，并且项目名正确。")
        return

    # 4. 启动心跳
    start_heartbeat(agent, interval=30)

    # 5. 发送上线消息
    agent.send_message(f"✅ {args.agent_name} 已接入，准备就绪！")

    print(f"\n🎉 Agent已接入！在看板中 @{args.agent_id} 或 @{args.agent_name} 即可触发推送。")
    print(f"   按 Ctrl+C 退出。\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Agent已退出。")
        server.server_close()


if __name__ == "__main__":
    main()
