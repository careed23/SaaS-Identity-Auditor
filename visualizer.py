import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from datetime import datetime


def _get_latest_audit_report():
    list_of_files = glob.glob('audit_report_*.csv')
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)


def _load_history_report(history_dir, latest_file):
    history_files = glob.glob(os.path.join(history_dir, 'audit_report_*.csv'))
    history_files = [path for path in history_files if os.path.abspath(path) != os.path.abspath(latest_file)]
    if not history_files:
        return None
    return max(history_files, key=os.path.getctime)


def _calculate_risk_trend(current_df, previous_df):
    current_risk = current_df['risk_score'].sum()
    previous_risk = previous_df['risk_score'].sum()
    if current_risk < previous_risk:
        return "Improving", current_risk, previous_risk
    if current_risk > previous_risk:
        return "Worsening", current_risk, previous_risk
    return "Stable", current_risk, previous_risk


def generate_dashboard():
    # 1. Find the latest CSV report automatically
    latest_file = _get_latest_audit_report()
    if not latest_file:
        print("[-] No audit reports found. Please run auditor.py first.")
        return

    print(f"[+] Visualizing data from: {latest_file}")

    # 2. Load the data
    try:
        df = pd.read_csv(latest_file)
    except Exception as e:
        print(f"[-] Error reading CSV: {e}")
        return

    history_dir = "history"
    previous_file = _load_history_report(history_dir, latest_file)
    trend_label = "No History"
    trend_details = None
    if previous_file:
        try:
            previous_df = pd.read_csv(previous_file)
            trend_label, current_risk, previous_risk = _calculate_risk_trend(df, previous_df)
            trend_details = {
                "label": trend_label,
                "current": current_risk,
                "previous": previous_risk,
                "file": previous_file
            }
        except Exception as e:
            print(f"[-] Error reading historical CSV: {e}")

    # --- ADVANCED STAFF ENGINEER ANALYTICS ---

    # Metric A: Risk by Department (Who is the worst offender?)
    # Grouping by department allows us to target remediation efforts.
    dept_risk = df.groupby('department')['risk_score'].sum().sort_values(ascending=True)

    # Metric B: Global MFA Compliance (The C-Level Metric)
    mfa_counts = df['mfa_enabled'].value_counts()

    # Metric C: Specific Violation Types (Operational View)
    stale_count = df['violation_stale'].sum()
    shadow_admin_count = df['violation_shadow_admin'].sum()

    # --- DASHBOARD LAYOUT & STYLING ---

    # Use a professional style sheet
    plt.style.use('ggplot')

    # Create a figure with a custom layout (2 rows, 2 columns)
    fig = plt.figure(figsize=(14, 10))
    title_parts = [f'Enterprise Identity Risk Dashboard\nSource: {latest_file}']
    if trend_details:
        title_parts.append(
            f"Risk Trend: {trend_details['label']} (Current {trend_details['current']}, Prior {trend_details['previous']})"
        )
    fig.suptitle("\n".join(title_parts), fontsize=20, fontweight='bold', color='#333333')

    # Subplot 1: MFA Compliance (Donut Chart) - Top Right
    # Executive view: "How secure are we generally?"
    ax1 = fig.add_subplot(2, 2, 2)
    labels = ['MFA Enabled', 'No MFA']
    # Ensure we match the boolean index correctly
    sizes = [mfa_counts.get(True, 0), mfa_counts.get(False, 0)]
    colors_mfa = ['#2ca02c', '#d62728']  # Green vs Red

    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       startangle=90, colors=colors_mfa, pctdistance=0.85,
                                       textprops={'fontsize': 12})

    # Draw a circle at the center to turn pie into donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax1.add_artist(centre_circle)
    ax1.set_title('Global MFA Compliance Rate', fontsize=14, fontweight='bold')

    # Subplot 2: Risk Score by Department (Horizontal Bar) - Left Side (Spans 2 rows if we wanted, but let's do Top Left)
    # Tactical view: "Who do I need to email today?"
    ax2 = fig.add_subplot(2, 2, 1)
    dept_risk.plot(kind='barh', color='#ff7f0e', ax=ax2, edgecolor='black', alpha=0.8)
    ax2.set_title('Cumulative Risk Score by Department', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Total Risk Points')
    ax2.set_ylabel('Department')

    # Subplot 3: Specific Violations (Grouped Bar) - Bottom (Spans entire width)
    # Operational view: "What specific problems are we facing?"
    ax3 = fig.add_subplot(2, 1, 2)
    categories = ['Stale Accounts\n(>90 Days)', 'Shadow Admins\n(Privileged + No MFA)']
    values = [stale_count, shadow_admin_count]

    bars = ax3.bar(categories, values, color=['#9467bd', '#d62728'], width=0.4, edgecolor='black')
    ax3.set_title('Critical Security Violations Breakdown', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Number of Users')
    ax3.grid(axis='y', linestyle='--', alpha=0.5)

    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    if trend_details:
        ax3.text(0.98, 0.95,
                 f"Risk Trend: {trend_details['label']}\nCurrent: {trend_details['current']}\nPrior: {trend_details['previous']}",
                 transform=ax3.transAxes, ha='right', va='top', fontsize=11,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8, edgecolor='gray'))
    elif trend_label == "No History":
        ax3.text(0.98, 0.95,
                 "Risk Trend: No historical report available",
                 transform=ax3.transAxes, ha='right', va='top', fontsize=11,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8, edgecolor='gray'))

    # Footer with timestamp (Audit Trail)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.5, 0.02, f'Generated by SaaS-Identity-Auditor | {timestamp}',
                ha='center', fontsize=10, color='gray')

    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save
    output_image = "security_dashboard_advanced.png"
    plt.savefig(output_image, dpi=150)  # Higher DPI for professional reports
    print(f"[+] Advanced Dashboard generated: {output_image}")


if __name__ == "__main__":
    generate_dashboard()
