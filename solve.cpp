#include <bits/stdc++.h>
#define MAXN 3005
using namespace std;
int N, W;
int h[MAXN];
int w[MAXN];
int dp[MAXN][MAXN];
int main(){
	cin >> N >> W;
	for (int i = 1; i <= N; i++)
		cin >> h[i] >> w[i], dp[i][w[i]] = 1;

	for (int i = 1; i <= N; i++)
		for (int j = w[i]; j <= W; j++)
			for (int k = 1; k < i; k++)
				if (h[k] < h[i])
					dp[i][j] = max(dp[i][j], dp[k][j - w[i]] + 1);
	int ans = 0;
	for (int i = 1; i <= W; i++)
		for (int j = 0; j <= N; j++)
			ans = max(ans, dp[j][i]);
	cout << ans << endl;

	return 0;
}